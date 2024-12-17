import argparse
import asyncio
import json
import mimetypes
import ntpath
import os
import platform
import re
import time
import traceback
from datetime import datetime, timezone

import aiofiles
import httpx
from tqdm import tqdm

__version__ = "2.0.12"
CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), ".canvassyncer.json"
)
PAGES_PER_TIME = 8


class AsyncSemClient:
    def __init__(self, connectionCount, token, proxy):
        self.sem = asyncio.Semaphore(connectionCount)
        self.client = httpx.AsyncClient(
            timeout=5,
            headers={"Authorization": f"Bearer {token}"},
            proxy=proxy,
            transport=httpx.AsyncHTTPTransport(retries=3),
            follow_redirects=True,
        )

    async def downloadOne(self, src, dst):
        async with self.sem:
            async with self.client.stream("GET", src) as res:
                if res.status_code >= 400:
                    return self.failures.append(f"{src} => {dst}")
                num_bytes_downloaded = res.num_bytes_downloaded
                dst_temp = dst + ".temp"
                try:
                    async with aiofiles.open(dst_temp, "+wb") as f:
                        async for chunk in res.aiter_bytes():
                            await f.write(chunk)
                            self.tqdm.update(
                                res.num_bytes_downloaded - num_bytes_downloaded
                            )
                            num_bytes_downloaded = res.num_bytes_downloaded
                except Exception as e:
                    print(e.__class__.__name__)
                    os.remove(dst_temp)
                    return
                os.rename(dst_temp, dst)

    async def downloadMany(self, infos, totalSize=0):
        self.tqdm = tqdm(total=totalSize, unit="B", unit_scale=True)
        self.failures = []
        await asyncio.gather(
            *[asyncio.create_task(self.downloadOne(src, dst)) for src, dst in infos]
        )
        self.tqdm.close()
        if self.failures:
            print(f"Fail to download these {len(self.failures)} file(s):")
            for text in self.failures:
                print(text)

    async def json(self, *args, **kwargs):
        retryTimes = 0
        checkError = bool(kwargs.pop("checkError", False))
        debugMode = bool(kwargs.pop("debug", False))
        while retryTimes <= 5:
            try:
                async with self.sem:
                    resp = await self.client.get(*args, **kwargs)
                res = resp.json()
                if checkError and isinstance(res, dict) and res.get("errors"):
                    errMsg = res["errors"][0].get("message", "unknown error.")
                    print(f"\nError: {errMsg}")
                    exit(1)
                return res
            except Exception as e:
                retryTimes += 1
                if debugMode:
                    print(f"{e.__class__.__name__}. Retry. {retryTimes} times.")

    async def head(self, *args, **kwargs):
        async with self.sem:
            resp = await self.client.head(*args, **kwargs)
        return resp.headers

    async def aclose(self):
        await self.client.aclose()


class CanvasSyncer:
    def __init__(self, config):
        self.config = config
        self.client = AsyncSemClient(
            config["connection_count"], config["token"], config.get("proxy")
        )
        self.downloadSize = 0
        self.laterDownloadSize = 0
        self.courseCode = {}
        self.baseUrl = self.config["canvasURL"] + "/api/v1"
        self.downloadDir = self.config["downloadDir"]
        self.newInfo = []
        self.newFiles = []
        self.laterFiles = []
        self.laterInfo = []
        self.skipfiles = []
        self.totalFileCount = 0
        if not os.path.exists(self.downloadDir):
            os.mkdir(self.downloadDir)

    async def aclose(self):
        await self.client.aclose()

    async def dictFromPages(self, helperFunc, *args, **kwargs):
        res = {}
        page = 1
        endOfPage = False
        while not endOfPage:
            pageRes = await asyncio.gather(
                *[helperFunc(page + i, *args, **kwargs) for i in range(PAGES_PER_TIME)]
            )
            for item in pageRes:
                if not item:
                    endOfPage = True
                res.update(item)
            page += PAGES_PER_TIME
        return res

    def prepareLocalFiles(self, courseID, folders):
        localFiles = []
        for folder in folders.values():
            if self.config["no_subfolder"]:
                path = os.path.join(self.downloadDir, folder[1:])
            else:
                path = os.path.join(
                    self.downloadDir, f"{self.courseCode[courseID]}{folder}"
                )
            if not os.path.exists(path):
                os.makedirs(path)
            localFiles += [
                os.path.join(folder, f).replace("\\", "/").replace("//", "/")
                for f in os.listdir(path)
                if not os.path.isdir(os.path.join(path, f))
            ]
        return localFiles

    async def getCourseFoldersWithIDHelper(self, page, courseID):
        res = {}
        url = f"{self.baseUrl}/courses/{courseID}/folders?page={page}"
        retryTimes = 0
        while retryTimes < 5:
            try:
                folders = await self.client.json(url, debug=self.config["debug"])
                for folder in folders:
                    if folder["full_name"].startswith("course files"):
                        folder["full_name"] = folder["full_name"][len("course files") :]
                    res[folder["id"]] = folder["full_name"]
                    if not res[folder["id"]]:
                        res[folder["id"]] = "/"
                    res[folder["id"]] = re.sub(
                        r"[\\\:\*\?\"\<\>\|]", "_", res[folder["id"]]
                    )
                return res
            except Exception as e:
                retryTimes = retryTimes + 1
                if self.config["debug"]:
                    print(str(retryTimes) + " time(s) error: " + str(e))

    async def getCourseFilesHelper(self, page, courseID, folders):
        files = {}
        url = f"{self.baseUrl}/courses/{courseID}/files?page={page}"
        canvasFiles = await self.client.json(url, debug=self.config["debug"])
        if not canvasFiles or isinstance(canvasFiles, dict):
            return files
        for f in canvasFiles:
            if f["folder_id"] not in folders.keys():
                continue
            f["display_name"] = re.sub(r"[\/\\\:\*\?\"\<\>\|]", "_", f["display_name"])
            path = f"{folders[f['folder_id']]}/{f['display_name']}"
            path = path.replace("\\", "/").replace("//", "/")
            dt = datetime.strptime(f["modified_at"], "%Y-%m-%dT%H:%M:%SZ")
            modifiedTimeStamp = dt.replace(tzinfo=timezone.utc).timestamp()
            files[path] = (f["url"], int(modifiedTimeStamp))
        return files

    async def getCourseFiles(self, courseID):
        folders = await self.dictFromPages(self.getCourseFoldersWithIDHelper, courseID)
        files = await self.dictFromPages(self.getCourseFilesHelper, courseID, folders)
        return folders, files

    async def getCourseIdByCourseCodeHelper(self, page, lowerCourseCodes):
        res = {}
        url = f"{self.baseUrl}/courses?page={page}"
        courses = await self.client.json(
            url, checkError=True, debug=self.config["debug"]
        )
        if not courses:
            return res
        for course in courses:
            if course.get("course_code", "").lower() in lowerCourseCodes:
                res[course["id"]] = course["course_code"]
                lowerCourseCodes.remove(course.get("course_code", "").lower())
        return res

    async def getCourseIdByCourseCode(self):
        lowerCourseCodes = [s.lower() for s in self.config["courseCodes"]]
        self.courseCode = await self.dictFromPages(
            self.getCourseIdByCourseCodeHelper, lowerCourseCodes
        )

    async def getCourseCodeByCourseIDHelper(self, courseID):
        url = f"{self.baseUrl}/courses/{courseID}"
        clientRes = await self.client.json(url, debug=self.config["debug"])
        if clientRes.get("course_code") is None:
            return
        self.courseCode[courseID] = clientRes["course_code"]

    async def getCourseCodeByCourseID(self):
        await asyncio.gather(
            *[
                asyncio.create_task(self.getCourseCodeByCourseIDHelper(courseID))
                for courseID in self.config["courseIDs"]
            ]
        )

    async def getCourseID(self):
        coros = []
        if self.config.get("courseCodes"):
            coros.append(self.getCourseIdByCourseCode())
        if self.config.get("courseIDs"):
            coros.append(self.getCourseCodeByCourseID())
        await asyncio.gather(*coros)

    async def getCourseTaskInfoHelper(
        self, courseID, localFiles, fileName, fileUrl, fileModifiedTimeStamp
    ):
        if not fileUrl:
            return
        if self.config["no_subfolder"]:
            path = os.path.join(self.downloadDir, fileName[1:])
        else:
            path = os.path.join(
                self.downloadDir, f"{self.courseCode[courseID]}{fileName}"
            )
        path = path.replace("\\", "/").replace("//", "/")
        if fileName in localFiles and fileModifiedTimeStamp <= os.path.getctime(path):
            return
        response = await self.client.head(fileUrl)
        fileSize = int(response.get("content-length", 0))
        if fileName in localFiles:
            self.laterDownloadSize += fileSize
            self.laterFiles.append((fileUrl, path))
            self.laterInfo.append(
                f"{self.courseCode[courseID]}{fileName} ({round(fileSize / 1000000, 2)}MB)"
            )
            return
        if fileSize > self.config["filesizeThresh"] * 1000000:
            aiofiles.open(path, "w").close()
            self.skipfiles.append(
                f"{self.courseCode[courseID]}{fileName} ({round(fileSize / 1000000, 2)}MB)"
            )
            return
        self.newInfo.append(
            f"{self.courseCode[courseID]}{fileName} ({round(fileSize / 1000000, 2)}MB)"
        )
        self.downloadSize += fileSize
        self.newFiles.append((fileUrl, path))

    async def getCourseTaskInfo(self, courseID):
        folders, files = await self.getCourseFiles(courseID)
        self.totalFileCount += len(files)
        localFiles = self.prepareLocalFiles(courseID, folders)
        await asyncio.gather(
            *[
                self.getCourseTaskInfoHelper(
                    courseID, localFiles, fileName, fileUrl, fileModifiedTimeStamp
                )
                for fileName, (fileUrl, fileModifiedTimeStamp) in files.items()
            ]
        )

    def checkNewFiles(self):
        if self.skipfiles:
            print(
                "These file(s) will not be synced due to their size"
                + f" (over {self.config['filesizeThresh']} MB):"
            )
            for f in self.skipfiles:
                print(f)
        if self.newFiles:
            print(f"Start to download {len(self.newInfo)} file(s)!")
            for s in self.newInfo:
                print(s)

    def checkLaterFiles(self):
        if not self.laterFiles:
            return
        print("These file(s) have later version on canvas:")
        for s in self.laterInfo:
            print(s)
        isDownload = "Y" if self.config["y"] else input("Update all?(Y/n) ")
        if isDownload in ["n", "N"]:
            return
        print(f"Start to download {len(self.laterInfo)} file(s)!")
        laterFiles = []
        for fileUrl, path in self.laterFiles:
            localCreatedTimeStamp = int(os.path.getctime(path))
            try:
                newPath = os.path.join(
                    ntpath.dirname(path),
                    f"{localCreatedTimeStamp}_{ntpath.basename(path)}",
                )
                if self.config["no_keep_older_version"]:
                    os.remove(path)
                elif not os.path.exists(newPath):
                    os.rename(path, newPath)
                else:
                    path = os.path.join(
                        ntpath.dirname(path),
                        f"{int(time.time())}_{ntpath.basename(path)}",
                    )
                laterFiles.append((fileUrl, path))
            except Exception as e:
                print(f"{e.__class__.__name__}! Skipped: {path}")
        self.laterFiles = laterFiles

    def checkAllowDownload(self, filename):
        fileType = (mimetypes.guess_type(filename))[0]
        if fileType is None:
            return True
        if not self.config["allowAudio"]:
            if fileType.split("/")[0] == "audio":
                print(
                    f"Remove {filename} from the download list because of its file type: audio."
                )
                return False
        if not self.config["allowVideo"]:
            if fileType.split("/")[0] == "video":
                print(
                    f"Remove {filename} the download list because of its file type: video."
                )
                return False
        if not self.config["allowImage"]:
            if fileType.split("/")[0] == "image":
                print(
                    f"Remove {filename} the download list because of its file type: image."
                )
                return False
        return True

    def checkFilesType(self):
        self.laterFiles = [
            (fileUrl, path)
            for (fileUrl, path) in self.laterFiles
            if self.checkAllowDownload(path)
        ]
        self.newFiles = [
            (fileUrl, path)
            for (fileUrl, path) in self.newFiles
            if self.checkAllowDownload(path)
        ]

    async def sync(self):
        print("Getting course IDs...")
        await self.getCourseID()
        print(f"Get {len(self.courseCode)} available courses!")
        print("Finding files on canvas...")
        await asyncio.gather(
            *[
                asyncio.create_task(self.getCourseTaskInfo(courseID))
                for courseID in self.courseCode.keys()
            ]
        )
        print(f"Get {self.totalFileCount} files!")
        if not self.newFiles and not self.laterFiles:
            return print("All local files are synced!")
        self.checkNewFiles()
        self.checkLaterFiles()
        self.checkFilesType()
        await self.client.downloadMany(
            self.newFiles + self.laterFiles, self.downloadSize + self.laterDownloadSize
        )


def initConfig():
    oldConfig = {}
    if os.path.exists(CONFIG_PATH):
        oldConfig = json.load(open(CONFIG_PATH))
    elif os.path.exists("./canvassyncer.json"):
        oldConfig = json.load(open("./canvassyncer.json"))

    def promptConfigStr(promptStr, key, *, defaultValOnMissing=None):
        defaultVal = oldConfig.get(key)
        if defaultVal is None:
            if defaultValOnMissing is not None:
                defaultVal = defaultValOnMissing
            else:
                defaultVal = ""
        elif isinstance(defaultVal, list):
            defaultVal = " ".join((str(val) for val in defaultVal))
        defaultVal = str(defaultVal)
        if defaultValOnMissing is not None:
            defaultValOnRemove = defaultValOnMissing
        else:
            defaultValOnRemove = ""
        tipStr = f"(Default: {defaultVal})" if defaultVal else ""
        tipRemove = "(If you input remove, value will become " + (
            f"{defaultValOnRemove})" if defaultValOnRemove != "" else "empty)"
        )
        res = input(f"{promptStr}{tipStr}{tipRemove}: ").strip()
        if not res:
            res = defaultVal
        elif res == "remove":
            res = defaultValOnRemove
        return res

    print("Generating new config file...")
    url = promptConfigStr(
        "Canvas url", "canvasURL", defaultValOnMissing="https://jicanvas.com"
    )
    token = promptConfigStr("Canvas access token", "token")
    courseCodesStr = promptConfigStr(
        "Courses to sync in course codes(split with space)", "courseCodes"
    )
    courseCodes = courseCodesStr.split()
    courseIDsStr = promptConfigStr(
        "Courses to sync in course ID(split with space)", "courseIDs"
    )
    courseIDs = [int(courseID) for courseID in courseIDsStr.split()]
    downloadDir = promptConfigStr(
        "Path to save canvas files",
        "downloadDir",
        defaultValOnMissing=os.path.abspath(""),
    )
    filesizeThreshStr = promptConfigStr(
        "Maximum file size to download(MB)", "filesizeThresh", defaultValOnMissing=250
    )
    allowAudio = promptConfigStr(
        "Whether allow downloading audios", "allowAudio", defaultValOnMissing=True
    )
    allowVideo = promptConfigStr(
        "Whether allow downloading videos", "allowVideo", defaultValOnMissing=True
    )
    allowImage = promptConfigStr(
        "Whether allow downloading images", "allowImage", defaultValOnMissing=True
    )

    try:
        filesizeThresh = float(filesizeThreshStr)
    except Exception:
        filesizeThresh = 250
    allowAudio = (allowAudio == "True") or (allowAudio == "true")
    allowVideo = (allowVideo == "True") or (allowVideo == "true")
    allowImage = (allowImage == "True") or (allowImage == "true")
    return {
        "canvasURL": url,
        "token": token,
        "courseCodes": courseCodes,
        "courseIDs": courseIDs,
        "downloadDir": downloadDir,
        "filesizeThresh": filesizeThresh,
        "allowAudio": allowAudio,
        "allowVideo": allowVideo,
        "allowImage": allowImage,
    }


def getConfig():
    parser = argparse.ArgumentParser(description="A Simple Canvas File Syncer")
    parser.add_argument("-r", help="recreate config file", action="store_true")
    parser.add_argument("-y", help="confirm all prompts", action="store_true")
    parser.add_argument(
        "--no-subfolder",
        help="do not create a course code named subfolder when synchronizing files",
        action="store_true",
    )
    parser.add_argument(
        "-p", "--path", help="appoint config file path", default=CONFIG_PATH
    )
    parser.add_argument(
        "-c",
        "--connection",
        help="max connection count with server",
        default=16,
        type=int,
    )
    parser.add_argument("-x", "--proxy", help="download proxy", default=None)
    parser.add_argument("-V", "--version", action="version", version=__version__)
    parser.add_argument(
        "-d", "--debug", help="show debug information", action="store_true"
    )
    parser.add_argument(
        "--no-keep-older-version",
        help="do not keep older version",
        action="store_true",
    )
    args = parser.parse_args()
    configPath = args.path
    if args.r or not os.path.exists(configPath):
        if not os.path.exists(configPath):
            print("Config file not exist, creating...")
        try:
            json.dump(
                initConfig(),
                open(configPath, mode="w", encoding="utf-8"),
                indent=4,
            )
        except Exception as e:
            print(f"\nError: {e.__class__.__name__}. Failed to create config file.")
            if args.debug:
                print(traceback.format_exc())
            exit(1)
    config = json.load(open(configPath, mode="r", encoding="utf-8"))
    config["y"] = args.y
    config["proxy"] = args.proxy
    config["no_subfolder"] = args.no_subfolder
    config["connection_count"] = args.connection
    config["no_keep_older_version"] = args.no_keep_older_version
    config["debug"] = args.debug
    if not "allowAudio" in config:
        config["allowAudio"] = True
    if not "allowVideo" in config:
        config["allowVideo"] = True
    if not "allowImage" in config:
        config["allowImage"] = True

    return config


async def sync():
    syncer = None
    try:
        config = getConfig()
        while True:
            try:
                syncer = CanvasSyncer(config)
                await syncer.sync()
                break
            except httpx.ConnectError as e:
                if config["connection_count"] == 2:
                    raise e
                config["connection_count"] //= 2
                print(
                    "Server connect error, reducing connection count "
                    f"to {config['connection_count']} and retrying..."
                )
    except KeyboardInterrupt as e:
        raise e
    except Exception as e:
        errorName = e.__class__.__name__
        print(
            f"Unexpected error: {errorName}. Please check your network and token!"
            + ("" if config["debug"] else " Or use -d for detailed information.")
        )
        if config["debug"]:
            print(traceback.format_exc())
    finally:
        if syncer:
            await syncer.aclose()


def run():
    try:
        if platform.system() == "Windows":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(sync())
    except KeyboardInterrupt:
        print("\nOperation cancelled by user, exiting...")
        exit(1)


if __name__ == "__main__":
    run()
