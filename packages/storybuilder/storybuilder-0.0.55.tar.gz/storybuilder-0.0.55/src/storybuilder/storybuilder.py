import json
import random
import os
import uuid
import copy

from .utility import *
from .storyprofiles import CHARACTER_FIGURE_ACCESSORY_KEYS, STORY_SCENARIO_STYLES
from .characterpostures import CHARACTER_FIGURES
from .storybase import *
from .postureselector import PostureSelector

PRODUCTION_ROOT="/story/"
TEST_ROOT="/test/"

class Story:

    def test(self, fileName="testStory.json", localOutputPath=LOCAL_DEFAULT_ROOT, incremental=True):
        for page in self._pages:
            page.exportAudios(
                localOutputPath=localOutputPath, 
                synthesizer=self._synthesizer, 
                cosUploader=self._cosUploader, 
                uploadToCos=True, 
                incremental=incremental
            )

        with open(os.path.join(localOutputPath, fileName), "w") as file:
            json.dump(
                self.export(), file, ensure_ascii=False, indent=4, sort_keys=False
            )
        print(f"Story.test exported to {os.path.join(localOutputPath, fileName)}")
    
    def export(self, debug=False):
        voices = [{"sound": ENDING_SOUND}]
        events = []
        for i, page in enumerate(self._pages):
            if debug:
                print(f"Story.export(), page{i} type {BLUE}{page.pageType}{RESET}")
            pageObject = page.export(voiceOffset=len(voices), pageId=float(len(events)))
            if isinstance(pageObject, dict) \
                and "voices" in pageObject and "events" in pageObject:
                for entry in pageObject["voices"]:
                    entryObject = {}
                    if isinstance(entry, dict):
                        for key in set(entry.keys()) & {"sound", "languages"}:
                            if entry[key] != None:
                                entryObject[key] = entry[key]
                        if len(entryObject) > 0:
                            voices.append(entryObject)
                events = events + pageObject["events"]

        return {"voices": voices, "events": events}

    def exportScripts(self):
        voices = []
        for i, page in enumerate(self._pages):
            pageObject = page.export(voiceOffset=len(voices))
            pageVoices = []
            for voice in pageObject["voices"]:
                if isinstance(voice, dict) \
                    and isinstance(voice.get("transcript", None), (str, dict)) \
                    and len(voice["transcript"]) > 0:
                    pageVoices.append(voice)
            if len(pageVoices) > 0:
                voices = voices + [{"page": i, "voices": pageVoices}]

        return voices

    def exportAudios(self, localOutputPath=LOCAL_DEFAULT_ROOT, uploadToCos=True, incremental=True):
        for page in self._pages:
            page.exportAudios(
                localOutputPath=localOutputPath, 
                synthesizer=self._synthesizer, 
                cosUploader=self._cosUploader, 
                uploadToCos=uploadToCos,
                incremental=incremental
            )

    def exportProduct(self, fileName=None, localOutputPath='./prod'):
        if self._cosUploader == None:
            print("Cos uploader is not available, exit.")
            return

        if not os.path.exists(localOutputPath):
            os.makedirs(localOutputPath)

        storyObject = self.export()
        
        # Copy audios to product path
        for i, voice in enumerate(storyObject["voices"]):
            defaultFileName = voice["sound"]
            storyObject["voices"][i]["sound"] = self._cosUploader.test2product(defaultFileName)
            if isinstance(storyObject["voices"][i].get("languages", None), list) and len(storyObject["voices"][i]["languages"]) > 0:
                for language in storyObject["voices"][i]["languages"]:
                    lingualFileName = defaultFileName[:-3] + language + '.mp3'
                    self._cosUploader.test2product(lingualFileName)


        # Copy images to product path
        for j, event in enumerate(storyObject["events"]):
            if "board" in event and isinstance(event["board"], dict):
                board = event["board"]
                if isinstance(board.get("content", None), dict):
                    if isinstance(board["content"].get("image", None), str) \
                    and len(board["content"]["image"]) > 0:
                        storyObject["events"][j]["board"]["content"]["image"] = self._cosUploader.test2product(board["content"]["image"])
                    elif isinstance(board["content"].get("image", None), dict) \
                    and len(board["content"]["image"]) > 0:
                        for language in board["content"]["image"].keys():
                            storyObject["events"][j]["board"]["content"]["image"][language] = self._cosUploader.test2product(board["content"]["image"][language])
                if isinstance(board.get("contentList", None), list) \
                    and len(board["contentList"]) > 0:
                    for k, contentEntry in enumerate(board["contentList"]):
                        if isinstance(contentEntry.get("image", None), str) \
                            and len(contentEntry["image"]) > 0:
                            storyObject["events"][j]["board"]["contentList"][k]["image"] = self._cosUploader.test2product(contentEntry["image"])
                        elif isinstance(contentEntry.get("image", None), dict) \
                            and len(contentEntry["image"]) > 0:
                            for language in contentEntry["image"].keys():
                                storyObject["events"][j]["board"]["contentList"][k]["image"][language] = self._cosUploader.test2product(contentEntry["image"][language])

        productFileName = fileName if fileName != None else os.path.join(localOutputPath, self.title + ".product.json")
        with open(productFileName, "w") as file:
            json.dump(
                storyObject, file, ensure_ascii=False, indent=4, sort_keys=False
            )
        print(f"Story resource copied from test to production, product story generated as {productFileName}.")

    @staticmethod
    def buildStoryCollection(outputName, storyList):
        storyCollection = {"collection": []}
        for story in storyList:
            storyTitle = story[:len(story)-5] if story.endswith(".json") else story
            storyCollection["collection"].append(storyTitle)
        with open(outputName, "w") as file:
            json.dump(
                storyCollection, file, ensure_ascii=False, indent=4, sort_keys=False
            )
    
    @staticmethod
    def loadFromFile(fileName, locale=DEFAULT_LANGUAGE, **kwargs):
        story = None
        storyId = None
        try:
            with open(fileName, 'r') as f:
                object = json.load(f)
            voices = object["voices"]
            events = object["events"]
            storyId = kwargs.get("storyId", None)
            if len(voices) > 1:
                for i in range(1, len(voices)):
                    folder = voices[i].get("sound", "//").split("/")[-2]
                    if len(folder) == 36: # length of uuid.uuid4()
                        storyId = folder
            storyStyle = None
            validScene = None
            for i in range(len(events)):
                if events[i].get("scene", None) != None and len(events[i]["scene"]) > 0:
                    validScene = events[i]["scene"]
                    break
            for styleKey in STORY_SCENARIO_STYLES.keys():
                for key, value in STORY_SCENARIO_STYLES[styleKey]["scenarios"].items():
                    if value == validScene \
                        or (key == "notes" and value["scene"] == validScene):
                        storyStyle = styleKey
                        break
            defaultNarrator = None
            for event in events:
                if defaultNarrator != None:
                    break
                if isinstance(event.get("objects", None), list):
                    _, _, defaultNarrator, _, _, _ = get_actors(event["objects"])
            kwargs["narrator"] = defaultNarrator if defaultNarrator != None else DEFAULT_NARRATOR
            story = Story(title=os.path.basename(fileName).replace(".json", ""), 
                        storyId=storyId, 
                        style=storyStyle, 
                        locale=locale, 
                        **kwargs)

            pageScenario = "cover"      # 没有样式匹配，设为CoverPage
            for event in events:
                # 获取页面类型
                if "board" in event \
                    and (
                        len(event["board"].get("type", '')) > 0 \
                        or (isinstance(event["board"].get("content", None), dict) \
                            and event["board"]["content"].get("type", None) != None) \
                        or (isinstance(event["board"].get("contentList", None), list) \
                            and any(isinstance(contentEntry, dict) and contentEntry.get('type', None) != None for contentEntry in event["board"]["contentList"])) \
                    ):
                    if isinstance(event["board"].get("contentList", None), list):
                        for entry in event["board"]["contentList"]:
                            if entry.get('type', None) != None:
                                pageScenario = entry['type']
                    pageScenario = event["board"]["type"] \
                        if event["board"].get("type", None) != None \
                        else (event["board"]["content"]["type"] \
                              if event["board"]["content"].get("type", None) != None \
                              else pageScenario)
                else:
                    sceneObject = event.get("scene", None)
                    if "index" in sceneObject and sceneObject["index"] == STORY_SCENARIO_STYLES[storyStyle]["scenarios"]["concentrak"]["index"]:
                        pageScenario = "concentrak"
                    elif isinstance(sceneObject, str) and len(sceneObject) > 0:
                        for key, value in STORY_SCENARIO_STYLES[storyStyle]["scenarios"].items():
                            if isinstance(value, str) and value == sceneObject:
                                pageScenario = key
                    elif "bgColor" in sceneObject and len(sceneObject["bgColor"]) > 0:
                        pageScenario = "blackboard"

                # 创建对应页面
                print(f"Loading page as {pageScenario}")
                # CoverPage
                if pageScenario == "cover":
                    story.createPage(
                        sceneType = pageScenario,
                        source = "",
                        voices = voices,
                        board = event.get("board", None),
                        objects = event.get("objects", None),
                        interactions = event.get("interactions", None)
                        )
                # ClassroomPage
                elif pageScenario == "classroom":
                    story.createPage(
                        sceneType = pageScenario,
                        voices = copy.deepcopy(voices),
                        board = event.get("board", None),
                        objects = event.get("objects", None),
                        interactions = event.get("interactions", None)
                        )
                # BlackboardPage
                elif pageScenario == "blackboard":
                    story.createPage(
                        sceneType = pageScenario,
                        source = "",
                        voices = copy.deepcopy(voices),
                        board = event.get("board", None),
                        objects = event.get("objects", None),
                        interactions = event.get("interactions", None)
                        )

                # ConcentrakPage
                elif pageScenario == "concentrak":
                    story.createPage(
                        sceneType = pageScenario,
                        text = "",
                        voices = copy.deepcopy(voices),
                        board = event.get("board", None),
                        objects = event.get("objects", None),
                        interactions = event.get("interactions", None)
                        )
                # ExamPage
                elif pageScenario == "exam":
                    story.createPage(
                        sceneType = pageScenario,
                        actor = "", 
                        voices = copy.deepcopy(voices),
                        board = event.get("board", None),
                        objects = event.get("objects", None),
                        interactions = event.get("interactions", None)
                    )

                # NotesPage
                elif pageScenario == "notes":
                    story.createPage(
                        sceneType = pageScenario,
                        actor = "", 
                        voices = copy.deepcopy(voices),
                        board = event.get("board", None),
                        objects = event.get("objects", None),
                        interactions = event.get("interactions", None)
                    )

                else:
                    pass            
            
        except Exception as e:
            print("Load story from file exception:\n", e)
            return None
            
        return story

    def __init__(self, title, storyId=None, style="shinkai_makoto", **kwargs):
        self.title = title
        self.storyId = storyId if storyId != None else str(uuid.uuid4())
        self.styles = STORY_SCENARIO_STYLES[style]
        self.locale = kwargs["locale"] if "locale" in kwargs else DEFAULT_LANGUAGE
        self.narrator = kwargs["narrator"] if "narrator" in kwargs else DEFAULT_NARRATOR
        self._pages = []
        self.posterPath = 'test/posters/'
        self.audioPath = 'test/audios/'

        self._cosUploader = kwargs.get("uploader", None)
        self._synthesizer = kwargs.get("synthesizer", None)

        self._defaultCharacters = CHARACTER_FIGURES

        self._postureSelector = PostureSelector() if kwargs.get("aiPosture", False) else None

        print(f"Create a new story title: {title}, Id:", self.storyId)

    def setStyle(self, styleName=None, styleObject=None):
        if isinstance(styleName, str) and styleName in STORY_SCENARIO_STYLES and styleName != self.styles:
            newStyles = STORY_SCENARIO_STYLES[styleName]
        elif isinstance(styleObject, dict):
            newStyles = merge_dicts(self.styles, styleObject)
        else:
            print("Not valid styleName or styleObject, return.")
            return

        for page in self._pages:
            page.applyStyle(newStyles)
        
        self.styles = newStyles

    def exportStyle(self):
        return copy.deepcopy(self.styles)

    def getAudioPath(self, fileName):
        return os.path.join("/", self.audioPath, self.storyId, fileName)

    def _getPosturePosition(self, actor, id):
        figureName = self._defaultCharacters[actor][id]
        if "boy" in figureName:
            if "half" in figureName:
                return self.styles["positions"]["right-bottom"]
            elif "standright" in figureName:
                return self.styles["positions"]["right"]
            elif "-stand-" in figureName:
                return self.styles["positions"]["left"]
            else: # head
                return [0, 0]
        elif "girl" in figureName:
            if "half" in figureName:
                return self.styles["positions"]["right-bottom"]
            elif "-stand-" in figureName:
                return self.styles["positions"]["right"]
            else: # head
                return [0, 0]
        else:
            return [0, 0]

        return [0, 0]
    def getUserPostureIdAndPosition(
        self, actor, postures, keyScenario="stand", excludeAccessories=True
    ):
        id = -1
        if type(postures) is int:
            id = postures
        elif type(postures) is list and type(postures[0]) is int:
            id = postures[0]
        elif self._defaultCharacters == None:
            id = 0
        else:
            currentActorFigures = self._defaultCharacters[actor]
            availableFigures = []
            for j, figure in enumerate(currentActorFigures):
                skip = False
                if excludeAccessories:
                    for accessory in CHARACTER_FIGURE_ACCESSORY_KEYS:
                        if accessory in figure:
                            skip = True
                if skip:
                    continue
                if keyScenario in figure and all(keyWord in figure for keyWord in (postures if isinstance(postures, list) else [postures])):
                    availableFigures.append({"index": j, "figure": figure})
            id = random.choice(availableFigures)["index"] if len(availableFigures) > 0 else 0
        return id, self._getPosturePosition(actor, id)

    def _NewPage(self, sceneType, **kwargs):
        try:
            scene = sceneType.lower()
        except Exception as e:
            print(f"problematic sceneType in type {type(sceneType)}: {sceneType}")
        newPage = None
        if scene == "classroom":
            newPage = ClassroomPage(self, **kwargs)
        elif scene == "blackboard":
            newPage = BlackboardPage(self, **kwargs)
        elif scene == "cover":
            newPage = CoverPage(self, **kwargs)
        elif scene == "exam":
            newPage = ExamPage(self, **kwargs)
        elif scene == "concentrak":
            newPage = ConcentrakPage(self, **kwargs)
        elif scene == "notes":
            newPage = NotesPage(self, **kwargs)
        else:
            print(f"Invalid scenario type {sceneType}, must be one of ('exam', 'notes', 'cover', 'blackboard', 'concentrak', 'classroom')")

        return newPage        

    def createPage(self, sceneType, **kwargs):
        newPage = self._NewPage(sceneType, **kwargs)

        if newPage != None:
            self._pages.append(newPage)

        return newPage

    def createPageAtPos(self, pos, sceneType, **kwargs):
        if pos >= 0 and pos < len(self._pages):
            newPage = self._NewPage(sceneType, **kwargs)
            if newPage != None:
                self._pages.insert(pos, newPage)
        else:
            print("Input pos is out of boundary.")
            newPage = None

        return newPage
    
    def removePageAtPos(self, pos):
        if pos >= 0  and pos < len(self._pages):
            self._pages.pop(pos)

    def getPage(self, pos):
        return self._pages[pos] if (pos >= 0  and pos < len(self._pages)) else None

    def uploadImageToCos(self, source, applyHash=True):
        if self._cosUploader != None:
            if isinstance(source, dict):
                for key in source:
                    source[key] = self._cosUploader.local2cos(source[key], self.storyId, self.posterPath, applyHash)
            else:
                source = self._cosUploader.local2cos(source, self.storyId, self.posterPath, applyHash)
        return source


class Page:
    def __init__(self, pageType, storyInstance):
        self.pageType = pageType
        self.story = storyInstance
        self.narrator = storyInstance.narrator
        self.locale = storyInstance.locale
        self.scene = None
        self.duration = None
        self.transition = None
        self.board = None
        self.objects = []
        self.transcripts = []
        self.mutescripts = []
        self.interactions = []
        self.defaultInteractions = []
        self.actor = None

    def applyStyle(self, styleObject):
        if "scenarios" in styleObject:
            if self.pageType in styleObject["scenarios"]:
                sceneValue = styleObject["scenarios"][self.pageType]
                if isinstance(sceneValue, str):
                    self.scene.value = sceneValue
                elif isinstance(sceneValue, dict):
                    if "scene" in sceneValue:
                        self.scene.value = sceneValue.get("scene", None) if isinstance(sceneValue.get("scene", None), str) else None
                        self.scene.index = sceneValue["scene"].get("index", None) if isinstance(sceneValue.get("scene", None), dict) else None
                        self.scene.bgColor = sceneValue["scene"].get("bgColor", None) if isinstance(sceneValue.get("scene", None), dict) else None
                    else:
                        self.scene.value = None
                        self.scene.index = sceneValue.get("index", None)
                        self.scene.bgColor = sceneValue.get("bgColor", None)

        if "frame" in styleObject:
            self.board.content.border = styleObject["frame"] if self.board.content.border!=None else None
            for i, content in enumerate(self.board.contentList):
                self.board.contentList[i].border = styleObject["frame"] if content.border!=None else None
        if "positions" in styleObject:
            oldPositions = self.story.styles["positions"]
            newPositions = styleObject["positions"]
            if oldPositions != newPositions:
                self.updateActorPosition(oldPositions, newPositions)
        if "popup" in styleObject:
            oldDialogPopup = self.story.styles["popup"]
            newDialogPopup = styleObject["popup"]
            if oldDialogPopup != newDialogPopup:
                self.updateDialogPopup(oldDialogPopup, newDialogPopup)
        if "transform" in styleObject:
            oldTransform = self.story.styles["transform"]
            newTransform = styleObject["transform"]
            if oldTransform != newTransform:
                self.updateActorTransform(oldTransform, newTransform)

    def updateActorPosition(self, oldPositions, newPositions):
        for i, interaction in enumerate(self.defaultInteractions):
            if isinstance(interaction, PostureInteraction):
                currentPositionKey = None
                for key in oldPositions:
                    if oldPositions[key] == interaction.position:
                        currentPositionKey = key
                        break
                if currentPositionKey in newPositions:
                    self.defaultInteractions[i].position = newPositions[currentPositionKey]

    def updateDialogPopup(self, oldDialogPopup, newDialogPopup):
        for i, interaction in enumerate(self.interactions):
            if interaction.content.popup == oldDialogPopup:
                self.interactions[i].content.popup = newDialogPopup
        for i, interaction in enumerate(self.defaultInteractions):
            if interaction.content.popup == oldDialogPopup:
                self.defaultInteractions[i].content.popup = newDialogPopup

    def updateActorTransform(self, oldTransform, newTransform):
        for i, interaction in enumerate(self.defaultInteractions):
            if isinstance(interaction, PostureInteraction) and interaction.transform == oldTransform:
                self.defaultInteractions[i].transform = newTransform

    def addHtml(self, html, rect=None):
        """Set HTML content for the page
        
        Args:
            html (Union[str, dict]): HTML content as string or multilingual dict
            rect (list, optional): Position and size of the HTML content. Defaults to None.
        """
        if isinstance(html, (str, dict)):
            # Always apply to content list
            if self.board.contentList is None:
                self.board.contentList = []
            if isinstance(self.board.contentList, list):
                self.board.contentList.append(Content(
                    html = MHTML.loadFromText(MText(html)),
                    rect = rect
                ))

    def updateHtml(self, pos, html, rect=None):
        """Update HTML content at specified position in contentList
        
        Args:
            pos (int): Position in contentList to update
            html (Union[str, dict]): New HTML content as string or multilingual dict
            rect (list, optional): New position and size of the HTML content. Defaults to None.
            
        Returns:
            bool: True if update successful, False otherwise
        """
        if isinstance(self.board.contentList, list) and pos < len(self.board.contentList) and pos >= 0:
            if self.board.contentList[pos].html is not None:
                self.board.contentList[pos].html = MHTML.loadFromText(MText(html))
                if rect is not None:
                    self.board.contentList[pos].rect = rect
                return True
        return False

    def removeHtml(self, pos):
        """Remove HTML content at specified position in contentList
        
        Args:
            pos (int): Position in contentList to remove
            
        Returns:
            bool: True if removal successful, False otherwise
        """
        if isinstance(self.board.contentList, list) and pos < len(self.board.contentList) and pos >= 0:
            if self.board.contentList[pos].html is not None:
                self.board.contentList.pop(pos)
                return True
        return False

    def _getUserId(self, actor):
        userId = -1
        for i, object in enumerate(self.objects):
            if object["name"].lower() == actor.lower():
                userId = i

        if userId == -1:
            self.objects.append({"name": actor})
            userId = len(self.objects) - 1
        return userId
    
    @staticmethod
    def fit_image_rect(rect, width, height, screenWidth=960.0, screenHeight=540.0):
        # image is wider in ratio
        if width / height > (rect[2] if rect[2] > 1.0 else rect[2]*screenWidth) / (rect[3] if rect[3] > 1.0 else rect[3]*screenHeight):
            height = round((rect[2] if rect[2] > 1.0 else rect[2]*screenWidth) * height / width / (1.0 if rect[3] > 1.0 else screenHeight), 3)
            width = rect[2] * 1.0
        # vice versa, rect is wider in ratio
        else:
            width = round((rect[3] if rect[3] > 1.0 else rect[3]*screenHeight) * width / height / (1.0 if rect[2] > 1.0 else screenWidth), 3)
            height = rect[3] * 1.0

        rect[0] += round(((rect[2] if rect[2] > 1.0 else rect[2]*screenWidth) \
                          - (width if width > 1.0 else width*screenWidth))/screenWidth/2.0, 3)
        rect[1] += round(((rect[3] if rect[3] > 1.0 else rect[3]*screenHeight) \
                          - (height if height > 1.0 else height*screenHeight))/screenHeight/2.0, 3)
        rect[2] = width if width > 1.0 else width * screenWidth
        rect[3] = height if height > 1.0 else height * screenHeight
        
        return rect

    def test(self, fileName="testPage.json", localOutputPath=LOCAL_DEFAULT_ROOT, incremental=True):
        if self.story==None:
            print(f"{RED}No story exists, return.{RESET}")
            return

        self.exportAudios(
            localOutputPath=localOutputPath, 
            synthesizer=self.story._synthesizer, 
            cosUploader=self.story._cosUploader, 
            uploadToCos=True, 
            incremental=incremental
        )

        with open(os.path.join(localOutputPath, fileName), "w") as file:
            json.dump(
                self.export(), file, ensure_ascii=False, indent=4, sort_keys=False
            )
        print(f"Page.test exported to {os.path.join(localOutputPath, fileName)}")

    def __audible_script_list__(self):
        return []

    def exportAudios(self, localOutputPath=LOCAL_DEFAULT_ROOT, synthesizer=None, cosUploader=None, uploadToCos=True, incremental=True):
        if self.story==None:
            print(f"{RED}No story exists, return.{RESET}")
            return
        directory = os.path.join(localOutputPath, self.story.storyId)
        if not os.path.exists(directory):
            os.makedirs(directory)

        currentSynthesizer = synthesizer if synthesizer!=None else self.story._synthesizer if self.story!=None else None
        currentCosUploader = cosUploader if cosUploader!=None else self.story._cosUploader if self.story!=None else None
        if currentCosUploader == None:
            print(f"{YELLOW}No COS uploader available, ignore uploading.{RESET}")

        if currentSynthesizer:
            for transcripts in self.__audible_script_list__():
                if len(transcripts) < 1:
                    continue
                for i, scriptObject in enumerate(transcripts):
                    if isinstance(scriptObject, Script):
                        if isinstance(scriptObject.sound, str) \
                            and (os.path.basename(scriptObject.sound) == scriptObject.sound or not incremental) \
                            and (not scriptObject.soundReady):
                            try:
                                fileName = os.path.basename(scriptObject.sound)
                                character = scriptObject.narrator
                                transcriptObject = MText(scriptObject.transcript).export()
                                alternativeObject = MText(scriptObject.alternative).export()
                                if isinstance(transcriptObject, str):
                                    transcriptStr = alternativeObject[DEFAULT_LANGUAGE] \
                                        if isinstance(alternativeObject, dict) \
                                            and len(alternativeObject.get(DEFAULT_LANGUAGE, '')) > 0 \
                                        else (
                                            alternativeObject \
                                                if isinstance(alternativeObject, str) \
                                                    and len(alternativeObject) > 0 \
                                                else transcriptObject
                                        )
                                    currentSynthesizer.synthesizeFile(
                                        character, remove_emojis(transcriptStr), DEFAULT_LANGUAGE, directory, fileName
                                    )
                                    localOutputFileName = os.path.join(directory, fileName)

                                    if currentCosUploader != None and uploadToCos:
                                        currentCosUploader.local2cos(localOutputFileName, self.story.storyId, self.story.audioPath)
                                        transcripts[i].sound = self.story.getAudioPath(fileName)
                                    transcripts[i]._languages = None
                                elif isinstance(transcriptObject, dict):
                                    processedLanguages = []
                                    for language in transcriptObject:
                                        transcriptStr = alternativeObject[language] \
                                            if isinstance(alternativeObject, dict) \
                                                and len(alternativeObject.get(language, '')) > 0 \
                                            else (
                                                alternativeObject \
                                                    if language == DEFAULT_LANGUAGE \
                                                        and isinstance(alternativeObject, str) \
                                                        and len(alternativeObject) > 0 \
                                                    else transcriptObject[language]
                                            )
                                        if language != DEFAULT_LANGUAGE:
                                            fileName = fileName[:-3]+language+".mp3"                                            
                                        currentSynthesizer.synthesizeFile(
                                            character, remove_emojis(transcriptStr), language, directory, fileName
                                        )
                                        localOutputFileName = os.path.join(directory, fileName)

                                        if currentCosUploader != None and uploadToCos:
                                            currentCosUploader.local2cos(localOutputFileName, self.story.storyId, self.story.audioPath)
                                            if language == DEFAULT_LANGUAGE:
                                                transcripts[i].sound = self.story.getAudioPath(fileName)
                                            else:
                                                processedLanguages.append(language)
                                    transcripts[i]._languages = processedLanguages
                            except Exception as e:
                                print(f"Synthesize & upload script failed for [{scriptObject.transcript}]\n", e)
                                continue
        else:
            print(f"{RED}No synthesizer available, return.{RESET}")

    def export(self, voiceOffset, pageId):
        raise NotImplementedError("Subclasses must implement export()")

    def exportScripts(self):
        return self.export()["voices"]

##### 问答页面 #####
class ExamPage(Page):
    # onResult: -2
    class InitInteraction(Interaction):
        ON_RESULT = -2
        POPUP = 4
        def __init__(self, actorId=None, text=None, voice=None):
            super().__init__(onResult=self.ON_RESULT, actorId=actorId, type="talk", 
                                content=Content(
                                    popup=self.POPUP, 
                                    voice=voice, 
                                    text=text
                                )
                            )

    # onResult: -1
    class ErrorInteraction(Interaction):
        ON_RESULT = -1
        POPUP = 4
        def __init__(self, actorId=None, text=None, voice=None):
            super().__init__(onResult=self.ON_RESULT, actorId=actorId, type="talk",
                                content=Content(
                                    popup=self.POPUP, 
                                    voice=voice, 
                                    text=text
                                )
                            )

    # popup = 2, onResult: self.correctAnswerId
    class SuccessInteraction(Interaction):
        POPUP = 2
        def __init__(self, actorId=None, onResult=None, text=None, voice=None):
            super().__init__(onResult=onResult, actorId=actorId, type="talk", 
                                content=Content(
                                    popup=self.POPUP, 
                                    voice=voice, 
                                    text=text
                                )
                            )
    
    def __init__(self, storyInstance, actor=None, postures=["smilesay"], sound=None, **kwargs):
        super().__init__("exam", storyInstance)
        self.scene = Scene.load(self.story.styles["scenarios"][self.pageType])
        self.board = Board(type=self.pageType)
        self.defaultObject = self.pageType
        self.questionTranscript = None
        self.questionInteractions = []
        self.boardContentListScripts = []

        if all(key in kwargs for key in ("voices", "board", "objects", "interactions")):
            voices = kwargs["voices"]
            self.scene = Scene.load(kwargs["scene"]) if kwargs.get("scene", None) != None else self.scene
            self.board = Board.load(kwargs["board"])
            if self.board.content.options != None:
                count = len(MList(self.board.content.options).firstValidPair()[1])
                for i in range(count):
                    self.mutescripts.append(Script(transcript=self.board.content.options.getMTextByPos(i)))
            self.objects = kwargs["objects"]
            self.actor, actorId, _, _, _, _ = get_actors(self.objects)
            for interaction in kwargs["interactions"]:
                if isinstance(interaction, dict):
                    if ("figure" in interaction and interaction.get("figure", -1) > -1) and "position" in interaction:
                        self.defaultInteractions.append(PostureInteraction(
                            actorId = interaction["actor"] if interaction.get("actor", -1) > -1 else actorId,
                            position = interaction["position"],
                            figure = interaction["figure"],
                            transform = interaction["transform"] \
                                if (isinstance(interaction.get("transform", None), str) \
                                    and len(interaction["transform"]) > 0) \
                                else None
                        ))

                    # onResult in (-2, 0), initInteraction
                    if "content" in interaction and \
                        "onResult" in interaction and (interaction["onResult"][0] if isinstance(interaction["onResult"], list) else interaction["onResult"]) in (-2, 0):
                        content = interaction["content"]
                        if isinstance(content, dict) and "voice" in content:
                            voiceId = content["voice"]
                            self.soundFile = voices[voiceId]["sound"]
                            self.questionTranscript = Script(
                                sound = self.soundFile,
                                transcript = MText(self.board.content.question),
                                narrator = self.actor if self.actor!=None else self.narrator,
                                languages = voices[voiceId]["languages"] if "languages" in voices[voiceId] else None)
                            self.questionInteractions.append(ExamPage.InitInteraction(
                                actorId = self._getUserId(self.defaultObject),
                                text = MText(self.board.content.question) if self.board.content.question!=None else None,
                                voice = 0
                            ))
                    elif "onResult" in interaction:
                        onResultValue = (interaction["onResult"][0] if isinstance(interaction["onResult"], list) else interaction["onResult"])
                        textValue = interaction["content"].get("text", None) \
                            if ("content" in interaction and isinstance(interaction["content"], dict)) \
                            else None
                        
                        # onResultValue > 0, successInteraction
                        if onResultValue > 0:
                            self.correctAnswerId = onResultValue
                            if "content" in interaction and isinstance(interaction["content"].get("popup", None), int):
                                popup = interaction["content"]["popup"]
                                if popup == 2:
                                    self.questionInteractions.append(ExamPage.SuccessInteraction(
                                        actorId = self._getUserId(self.defaultObject),
                                        onResult = onResultValue,
                                        text = MText(textValue) if textValue!=None else None
                                    ))
                                if popup == 4:  # onSuccessPrompt, add to defaultInteractions
                                    self.defaultInteractions.append(Interaction(
                                        actorId = self._getUserId(self.defaultObject),
                                        onResult = onResultValue,
                                        content = Content(
                                            text = MText(textValue) if textValue!=None else None,
                                            popup = popup
                                        ),
                                        type = "talk"
                                    ))
                        # onResultValue == -1, errorInteraction
                        elif onResultValue == -1:
                            self.questionInteractions.append(ExamPage.ErrorInteraction(
                                actorId = self._getUserId(self.defaultObject),
                                text = MText(textValue) if textValue!=None else None
                            ))
                        if textValue!=None and len(textValue) > 0:
                            self.mutescripts.append(Script(transcript=MText(textValue)))
                    elif interaction.get("type", None) in ("motion", "talk") and "figure" in interaction:
                        postures = interaction["figure"]
                        if isinstance(interaction.get("content", None), dict) and "voice" in interaction["content"]:
                            content = interaction["content"]
                            voiceId = content["voice"]
                            if MText(content.get("text", "")) == self.board.content.question and voiceId > 0:
                                self.soundFile = voices[voiceId]["sound"]
                                self.questionTranscript = Script(
                                    sound = self.soundFile,
                                    transcript = self.board.content.question.copy(),
                                    narrator = self.actor if self.actor!=None else self.narrator,
                                    languages = voices[voiceId].get("languages", None)
                                )
                                                                
                                self.questionInteractions.append(ExamPage.InitInteraction(
                                    actorId = self._getUserId(self.defaultObject),
                                    text = self.board.content.question,
                                    voice = voiceId
                                ))
        else:
            if actor != None:
                self.setActor(actor, postures, **kwargs)
            self.soundFile = f"voice-{uuid.uuid4()}.mp3" if sound == None else sound
            
    def setActor(self, actor, postures=["smilesay"], **kwargs):
        if actor in VISIBLE_ACTORS:
            if self.actor != actor:
                update_visible_actor(self.objects, actor)
                if isinstance(self.questionTranscript, Script):
                    self.questionTranscript.reset2basename(actor)
                self.actor = actor

            posture_list = (
                [postures]
                if isinstance(postures, (str, int))
                else [postures[0]] \
                    if (isinstance(postures, list) and isinstance(postures[0], int))
                    else postures
            )
            figure, position = self.story.getUserPostureIdAndPosition(actor, posture_list, keyScenario="half")
            if isinstance(kwargs.get("position", None), list) and len(kwargs["position"]) == 2:
                position = kwargs["position"]
            scale = None
            if isinstance(kwargs.get("scale", None), (int, float)) and kwargs["scale"] > 0:
                scale = f"scale({kwargs['scale']})"
            hasPosture = False
            for i, interaction in enumerate(self.defaultInteractions):
                if isinstance(interaction, PostureInteraction):
                    self.defaultInteractions[i].actorId = self._getUserId(self.actor)
                    self.defaultInteractions[i].position = position
                    self.defaultInteractions[i].transform = scale if scale != None else interaction.transform
                    self.defaultInteractions[i].figure = figure
                    hasPosture = True
            if not hasPosture:
                self.defaultInteractions.append(PostureInteraction(
                    actorId = self._getUserId(self.actor),
                    position = position,
                    transform = scale if scale != None else "scale(1.5)",
                    figure = figure
                ))
        elif actor==None and self.actor!=None:
            for i, interaction in enumerate(self.defaultInteractions):
                if isinstance(interaction, PostureInteraction):
                    self.defaultInteractions.pop(i)
            if isinstance(self.questionTranscript, Script):
                self.questionTranscript.reset2basename(self.narrator)
            self.actor = None

    def setQuestion(self, question:MText, options:MList=[], answers=None, **kwargs):
        newQuestion = MText(question)
        newOptions = MList(options, DEFAULT_LANGUAGE)
        newAnswers = MList(answers, DEFAULT_LANGUAGE)

        hasChinese = False
        for i in range(len(newOptions.getListByLanguage(DEFAULT_LANGUAGE))):
            if has_chinese_char(newOptions.getListByLanguage(DEFAULT_LANGUAGE)[i]):
                hasChinese = True
            self.mutescripts.append(Script(transcript=newOptions.getMTextByPos(i)))

        if not hasChinese:
            newAnswers = MList(newAnswers.getListByLanguage(DEFAULT_LANGUAGE))
            newOptions = MList(newOptions.getListByLanguage(DEFAULT_LANGUAGE))

        fontSize = kwargs.get("fontSize", "20px")
        if isinstance(fontSize, int):
            fontSize = str(fontSize) + "px"

        self.board.content.fontSize=fontSize
        self.board.content.fontColor=kwargs.get("fontColor", "white")
        self.board.content.question=newQuestion if question != None else self.board.content.question
        self.board.content.options=newOptions
        self.board.content.answer=newAnswers
        self.board.content.colsPerRow=kwargs.get("colsPerRow", 1)
        self.board.rect=kwargs.get("rect", self.board.rect)

        self.correctAnswerId = 0
        for i, option in enumerate(newOptions.getListByLanguage(DEFAULT_LANGUAGE)):
            for entry in (newAnswers.getListByLanguage(DEFAULT_LANGUAGE)):
                if entry == option:
                    self.correctAnswerId += 2**i

        questionTranscript = kwargs.get("alternativeText", None) if kwargs.get("alternativeText", None)!=None else newQuestion
        # 如果新问题文字与原问题文字不同。则需先生成test语音，下一步再更新production上语音
        if self.questionTranscript == None:
            self.questionTranscript = Script(
                sound = f"voice-{uuid.uuid4()}.mp3",
                transcript = questionTranscript,
                narrator = self.actor if self.actor!=None else self.narrator
            )
        elif self.questionTranscript.transcript != questionTranscript:
            self.questionTranscript.transcript = questionTranscript
            self.questionTranscript.sound = f"voice-{uuid.uuid4()}.mp3" \
                if self.questionTranscript.sound == None or len(self.questionTranscript.sound) == 0 \
                else self.questionTranscript.sound
            self.questionTranscript.reset2basename(self.actor if self.actor!=None else self.narrator)

        #self.questionInteractions = []

        # 初始化页面行为 onResult: -2. 先删除旧事件，再添加新事件
        for questionInteraction in self.questionInteractions[:]:    # Use [:] to create a copy to avoid index issues
            if isinstance(questionInteraction, ExamPage.InitInteraction):
                self.questionInteractions.remove(questionInteraction)
        
        self.questionInteractions.append(ExamPage.InitInteraction(
            actorId = self._getUserId(self.defaultObject),
            text = self.board.content.question,
            voice = 0
        ))

        if isinstance(newOptions.firstValidPair()[1], list) and len(newOptions.firstValidPair()[1]) > 0:
            # 错误答案提示行为 onResult: -1. 先删除旧事件，再添加新事件
            for questionInteraction in self.questionInteractions[:]:
                if isinstance(questionInteraction, ExamPage.ErrorInteraction):
                    self.questionInteractions.remove(questionInteraction)

            self.questionInteractions.append(ExamPage.ErrorInteraction(
                actorId = self._getUserId(self.defaultObject),
                text = MText(kwargs.get("alwaysTruePrompt", kwargs.get("onErrorPrompt", {DEFAULT_LANGUAGE: "再想想"})))
            ))

            # 正确答案行为 onResult: 由所有正确答案id计算所得. 先删除旧事件，再添加新事件
            if self.correctAnswerId > 0:
                for questionInteraction in self.questionInteractions[:]:
                    if isinstance(questionInteraction, ExamPage.SuccessInteraction):
                        self.questionInteractions.remove(questionInteraction)

                self.questionInteractions.append(ExamPage.SuccessInteraction(
                    onResult=self.correctAnswerId,
                    actorId=self._getUserId(self.defaultObject)
                ))
                if kwargs.get("onSuccessPrompt", None) != None:
                    for defaultInteraction in self.defaultInteractions[:]:
                        if isinstance(defaultInteraction, Interaction) \
                            and (defaultInteraction.onResult != None \
                                 and defaultInteraction.onResult > 0):
                            self.defaultInteractions.remove(defaultInteraction)

                    self.defaultInteractions.append(Interaction(
                                            actorId = self._getUserId(self.defaultObject),
                                            onResult = self.correctAnswerId,
                                            content = Content(
                                                text = MText(kwargs["onSuccessPrompt"]),
                                                popup = 4
                                            ),
                                            type = "talk"
                                        ))
                    self.mutescripts.append(Script(transcript=MText(kwargs["onSuccessPrompt"])))

    def setFontSize(self, size):
        self.board.content.fontSize = str(size)+"px" if isinstance(size, int) else size

    def setColsPerRow(self, colsPerRow):
        self.board.content.colsPerRow = colsPerRow

    def setRect(self, rect):
        self.board.rect = rect

    def setFontColor(self, color):
        self.board.content.fontColor = color

    def addImage(self, source:Union[str, dict], rect:list=[0, 0, 1, 1], autoFit:bool=True, uploadToCos:bool=True, **kwargs):
        assert isinstance(rect, list) and len(rect) >= 4
        validUrl = False
        if is_valid_http_url(MText(source).firstValidPair()[1]):
            width = rect[2]
            height = rect[3]
            validUrl = True
        else:
            width, height = get_image_size(MText(source).firstValidPair()[1])
        assert width > 0 and height > 0
        mSource = MText(source) if source!=None else None
        mCaption = MText(kwargs.get("caption", "")) # Need value for caption to display image in contentList

        if not validUrl:
            if autoFit:
                rect = Page.fit_image_rect(rect, width, height)

            if uploadToCos:
                if isinstance(mSource.data, dict):
                    for key in mSource.data:
                        mSource.data[key] = self.story.uploadImageToCos(mSource.data[key], applyHash=kwargs.get("applyHash", True))
                else:
                    mSource.data = self.story.uploadImageToCos(mSource.data, applyHash=kwargs.get("applyHash", True))

        self.board.contentList.append(Content(
            image=mSource,
            rect=rect,
            caption=mCaption,
            magnify=kwargs.get("magnify", None),
            fontColor=kwargs.get("fontColor", None),
            fontSize=kwargs.get("fontSize", None)
        ))

        self.boardContentListScripts.append(Script(transcript=mCaption))

    def updateImage(self, pos:int, source:Union[str, dict], rect:list=[0, 0, 1, 1], autoFit:bool=True, uploadToCos:bool=True, **kwargs):
        if pos < len(self.board.contentList) and pos >= 0:
            assert isinstance(rect, list) and len(rect) >= 4
            validUrl = False
            if is_valid_http_url(MText(source).firstValidPair()[1]):
                width = rect[2]
                height = rect[3]
                validUrl = True
            else:
                width, height = get_image_size(MText(source).firstValidPair()[1])
            assert width > 0 and height > 0
            mSource = MText(source) if source!=None else None
            mCaption = MText(kwargs.get("caption", \
                                        self.board.contentList[pos].caption \
                                            if self.board.contentList[pos].caption != None \
                                            else ""
                                        )
                            )
            if isinstance(self.board.contentList[pos].caption, MText):
                mCaption = self.board.contentList[pos].caption.merge(mCaption)

            if not validUrl:
                if autoFit:
                    rect = Page.fit_image_rect(rect, width, height)

                if uploadToCos:
                    if isinstance(mSource.data, dict):
                        for key in mSource.data:
                            mSource.data[key] = self.story.uploadImageToCos(mSource.data[key], applyHash=kwargs.get("applyHash", True))
                    else:
                        mSource.data = self.story.uploadImageToCos(mSource.data, applyHash=kwargs.get("applyHash", True))

            self.board.contentList[pos].image = self.board.contentList[pos].image.merge(mSource)
            self.board.contentList[pos].rect = rect
            self.board.contentList[pos].caption = mCaption
            
            self.boardContentListScripts[pos] = Script(transcript=mCaption)

    def removeImage(self, pos):
        if pos < len(self.board.contentList) and pos >= 0:
            self.board.contentList.pop(pos)
            self.boardContentListScripts.pop(pos)

    def __audible_script_list__(self):
        return [[self.questionTranscript]]

    def export(self, voiceOffset=0, pageId=0.0):
        outTranscripts = [transcript.export() for transcript in ([self.questionTranscript] + self.boardContentListScripts + self.mutescripts) \
                         if (isinstance(transcript, Script) and transcript.export()!=None)]

        outInteractions = []
        for interaction in self.defaultInteractions + self.questionInteractions:
            newInteraction = None
            if interaction.content.voice != None and interaction.content.voice > -1:
                newInteraction = interaction.copy()
                newInteraction.content.voice += voiceOffset
            exported = newInteraction.export() if newInteraction != None else interaction.export() 
            if exported != None:
                outInteractions.append(exported)

        eventDict = {
            "id": pageId,
            "scene": self.scene.export(),
            "board": self.board.export(),
            "objects": copy.deepcopy(self.objects),
            "interactions": outInteractions
        }

        if self.duration is not None:
            eventDict["duration"] = self.duration

        if self.transition is not None:
            eventDict["transition"] = self.transition

        return {
            "voices": outTranscripts,
            "events": [eventDict]
        }

##### 总结页面 #####
class NotesPage(Page):
    def __init__(self, storyInstance, actor=None, postures=["smilesay"], endingEffect=True, sound=None, **kwargs):
        super().__init__("notes", storyInstance)
        self.scene = Scene.load(self.story.styles["scenarios"][self.pageType]["scene"])
        self.board = Board(
            content = Content(html=MHTML.loadFromText(self.story.styles["scenarios"][self.pageType]["htmlTemplate"])),
            rect = self.story.styles["scenarios"][self.pageType]["rect"],
            type = self.pageType
        )
        self.defaultObject = self.pageType

        if all(key in kwargs for key in ("voices", "board", "objects", "interactions")):
            voices = kwargs["voices"]
            self.scene = Scene.load(kwargs["scene"]) if kwargs.get("scene", None) != None else self.scene
            self.board = Board.load(kwargs["board"])
            self.objects = kwargs["objects"]
            self.actor, actorId, self.narrator, _, defaultObject, _ = get_actors(self.objects)
            self.defaultObject = defaultObject if defaultObject != None else self.narrator if self.narrator != None else self.defaultObject
            self.soundFile = f"voice-{uuid.uuid4()}.mp3" if sound == None else sound
            self.soundFileLanguages = None
            self.endingEffect = False
            postures = 0
            transform = None

            for interaction in kwargs["interactions"]:
                if isinstance(interaction, dict):
                    if isinstance(interaction.get("content", None), dict) and "voice" in interaction["content"]:
                        value = interaction["content"]["voice"]
                        if value == 0:
                            self.endingEffect = True
                        elif value > 0:
                            self.soundFile = voices[value]["sound"]
                            self.soundFileLanguages = voices[value].get("languages", None)
                    if "type" in interaction and "figure" in interaction:
                        value = interaction["figure"]
                        if interaction["type"] == "motion":
                            postures = value
                        elif interaction["type"] == "talk":
                            if interaction["actor"] == actorId and value > -1: 
                                postures = value
                        if "transform" in interaction:
                            transform = interaction["transform"]
            figure, position = self.story.getUserPostureIdAndPosition(self.actor, postures, keyScenario="half")
            self.defaultInteractions.append(
                PostureInteraction(
                    position = position,
                    transform = transform if transform != None else "scale(1.5)",
                    figure = figure,
                    actorId = actorId
                ))
            
        else:
            self.setActor(actor, postures, **kwargs)
            self.endingEffect = endingEffect
            self.soundFile = f"voice-{uuid.uuid4()}.mp3" if sound == None else sound
            self.soundFileLanguages = kwargs["languages"] if isinstance(kwargs.get("languages", None), list) else None

        self.endingInteraction = Interaction(
                duration = "auto",
                content = Content(
                    voice = 0,
                    text = MText("")
                ),
                actorId = self._getUserId(self.defaultObject),
                type = "talk"
            )

    def setActor(self, actor, postures=["smilesay"], **kwargs):
        if actor in VISIBLE_ACTORS:
            if self.actor != actor:
                update_visible_actor(self.objects, actor)
                [script.reset2basename(actor) for script in self.transcripts if isinstance(script, Script)]
                self.actor = actor

            posture_list = (
                [postures]
                if isinstance(postures, (str, int))
                else [postures[0]] \
                    if (isinstance(postures, list) and isinstance(postures[0], int))
                    else postures
            )
            figure, position = self.story.getUserPostureIdAndPosition(actor, posture_list, keyScenario="half")
            if isinstance(kwargs.get("position", None), list) and len(kwargs["position"]) == 2:
                position = kwargs["position"]
            scale = None
            if isinstance(kwargs.get("scale", None), (int, float)) and kwargs["scale"] > 0:
                scale = f"scale({kwargs['scale']})"
            hasPosture = False
            for i, interaction in enumerate(self.defaultInteractions):
                if isinstance(interaction, PostureInteraction):
                    self.defaultInteractions[i].actorId = self._getUserId(self.actor)
                    self.defaultInteractions[i].position = position
                    self.defaultInteractions[i].transform = scale if scale != None else interaction.transform
                    self.defaultInteractions[i].figure = figure
                    hasPosture = True
            if not hasPosture:
                self.defaultInteractions.append(PostureInteraction(
                    actorId = self._getUserId(self.actor),
                    position = position,
                    transform = scale if scale != None else "scale(1.5)",
                    figure = figure
                ))
        elif actor==None and self.actor!=None:
            for i, interaction in enumerate(self.defaultInteractions):
                if isinstance(interaction, PostureInteraction):
                    self.defaultInteractions.pop(i)
            self.actor = None

    def addBullet(self, text):
        if isinstance(self.board.content.html, MHTML):
            self.board.content.html.addBullet(text)
            self.soundFileLanguages = None
            if isinstance(self.soundFile, str):
                self.soundFile = switch_to_basename(self.soundFile)

    def updateBullet(self, pos, text):
        if isinstance(self.board.content.html, MHTML):
            if self.board.content.html.updateBullet(pos, text):
                self.soundFileLanguages = None
                if isinstance(self.soundFile, str):
                    self.soundFile = switch_to_basename(self.soundFile)

    def removeBullet(self, pos):
        if isinstance(self.board.content.html, MHTML):
            if self.board.content.html.removeBullet(pos):
                self.soundFileLanguages = None
                if isinstance(self.soundFile, str):
                    self.soundFile = switch_to_basename(self.soundFile)

    def setEndingEffect(self, on: bool):
        self.endingEffect = on

    def exportAudios(self, localOutputPath=LOCAL_DEFAULT_ROOT, synthesizer=None, cosUploader=None, uploadToCos=True, incremental=True):
        if self.story==None:
            print(f"{RED}No story exists, return.{RESET}")
            return
        directory = os.path.join(localOutputPath, self.story.storyId)
        if not os.path.exists(directory):
            os.makedirs(directory)

        currentSynthesizer = synthesizer if synthesizer!=None else self.story._synthesizer if self.story!=None else None
        currentCosUploader = cosUploader if cosUploader!=None else self.story._cosUploader if self.story!=None else None
        if currentCosUploader == None:
            print(f"{YELLOW}No COS uploader available, ignore uploading.{RESET}")

        if currentSynthesizer:
            if isinstance(self.soundFile, str) \
                and (os.path.basename(self.soundFile) == self.soundFile or not incremental):
                try:
                    fileName = os.path.basename(self.soundFile)
                    character = self.actor if self.actor!=None else self.narrator
                    transcriptObject = MText(self.board.content.html.exportScripts()).export()
                    if isinstance(transcriptObject, str):
                        transcriptStr = transcriptObject
                        currentSynthesizer.synthesizeFile(
                            character, remove_emojis(transcriptStr), DEFAULT_LANGUAGE, directory, fileName
                        )
                        localOutputFileName = os.path.join(directory, fileName)

                        if currentCosUploader != None and uploadToCos:
                            currentCosUploader.local2cos(localOutputFileName, self.story.storyId, self.story.audioPath)
                            self.soundFile = self.story.getAudioPath(fileName)
                        self.soundFileLanguages = None
                    elif isinstance(transcriptObject, dict):
                        transcriptDict = transcriptObject
                        processedLanguages = []
                        for language in transcriptDict:
                            transcriptStr = transcriptDict[language]
                            currentSynthesizer.synthesizeFile(
                                character, remove_emojis(transcriptStr), language, directory, fileName
                            )
                            localOutputFileName = os.path.join(directory, fileName)

                            if currentCosUploader != None and uploadToCos:
                                currentCosUploader.local2cos(localOutputFileName, self.story.storyId, self.story.audioPath)
                                self.soundFile = self.story.getAudioPath(fileName)
                                if language!=DEFAULT_LANGUAGE:
                                    processedLanguages.append(language)
                        self.soundFileLanguages = processedLanguages
                except Exception as e:
                    print(f"Synthesize & upload script failed for [{self.board.content.html.exportScripts()}]\n", e)
        else:
            print(f"{RED}No synthesizer available, return.{RESET}")

    def export(self, voiceOffset=0, pageId=0.0):
        outTranscripts = []
        if isinstance(self.board.content, Content) and self.board.content.export()!=None:
            contentScript = Script(
                sound=self.soundFile,
                transcript=MText(self.board.content.html.exportScripts()),
                narrator=self.actor if self.actor!=None else self.narrator,
                languages = self.soundFileLanguages if isinstance(self.soundFileLanguages, list) else None
                )
            outTranscripts.append(contentScript.export())
        if isinstance(self.board.contentList, list) and len(self.board.contentList) > 0:
            for i, entry in enumerate(self.board.contentList):
                entryScript = Script(
                    sound=self.soundFile if i==0 else None,
                    transcript=MText(entry.html.exportScripts()),
                    narrator=(self.actor if self.actor!=None else self.narrator) if i==0 else None,
                    languages = (self.soundFileLanguages if isinstance(self.soundFileLanguages, list) else None) if i==0 else None
                    )
                outTranscripts.append(entryScript.export())

        notesInteraction = Interaction(
                content = Content(
                    voice = 0 + voiceOffset
                ),
                type = "talk",
                actorId = self._getUserId(self.defaultObject)
            )
        outInteractions = [interaction.export() for interaction in (self.defaultInteractions + [notesInteraction] + ([self.endingInteraction] if self.endingEffect else []))]

        eventDict = {
            "id": pageId,
            "scene": self.scene.export(),
            "board": self.board.export(),
            "objects": copy.deepcopy(self.objects),
            "interactions": outInteractions
        }

        if self.duration is not None:
            eventDict["duration"] = self.duration

        if self.transition is not None:
            eventDict["transition"] = self.transition

        return {
            "voices": outTranscripts,
            "events": [eventDict]
        }


##### 概念页面 #####
class ConcentrakPage(Page):
    class ConcentrakInteraction(Interaction):
        def __init__(self, actorId=-1, text:MText=None):
            super().__init__(actorId=actorId, content=Content(popup=6, text=text))

    def __init__(self, storyInstance, **kwargs):
        super().__init__("concentrak", storyInstance)
        self.scene = Scene.load(self.story.styles["scenarios"][self.pageType])
        self.defaultObject = self.pageType

        if all(key in kwargs for key in ("voices", "board", "objects", "interactions")):
            voices = kwargs["voices"]
            self.objects = kwargs["objects"]
            self.scene = Scene.load(kwargs["scene"]) if kwargs.get("scene", None) != None else self.scene
            self.board = Board.load(kwargs["board"])
            for interaction in kwargs["interactions"]:
                if isinstance(interaction, dict):
                    if "content" in interaction:
                        content = interaction["content"]
                        if isinstance(content, dict):
                            if "popup" in content and "text" in content:
                                text = content["text"]
                                if content["popup"] == 6:
                                    self.setTitle(text)
                                elif content["popup"] == 4 and "voice" in content and content["voice"] > 0:
                                    voiceId = content["voice"]
                                    if "actor" in interaction:
                                        actorId = interaction["actor"]
                                        self.transcripts.append(Script(
                                            sound = voices[voiceId]["sound"],
                                            transcript = MText(text),
                                            narrator = self.objects[actorId]["name"],
                                            languages = voices[voiceId]["languages"] \
                                                if isinstance(voices[voiceId].get("languages", None), list) \
                                                else None 
                                            ))
                                        self.interactions.append(Interaction(
                                            duration = "auto",
                                            content = Content(
                                                popup = 4,
                                                text = MText(text),
                                                voice = len(self.transcripts) - 1
                                            ),
                                            actorId = actorId,
                                            type = "talk"))
        else:
            self.board = Board()
            if kwargs.get("title", None) != None:
                self.setTitle(kwargs["title"])
    
    def setTitle(self, text):
        if len(self.mutescripts) == 0:
            self.mutescripts.append(Script(transcript=MText(text)))
            self.defaultInteractions.append(ConcentrakPage.ConcentrakInteraction(
                    actorId = self._getUserId(self.defaultObject),
                    text = MText(text)
                ))
        else:
            self.mutescripts[0].transcript=MText(text)
            self.defaultInteractions[0].content.text = MText(text)

    def addNarration(self, text, narrator=None, alternativeText=None, sound=None, **kwargs):
        narrator = narrator if narrator != None else self.narrator if self.narrator != None else self.actor
        self.transcripts.append(Script(
            sound = f"voice-{uuid.uuid4()}.mp3" if sound == None else sound,
            transcript = MText(text),
            narrator = narrator,
            alternative = MText(alternativeText) if alternativeText!= None else None,
            languages = kwargs["languages"] if isinstance(kwargs.get("languages", None), list) else None,
            soundReady=bool(kwargs.get("soundReady", False))
            ))          
        
        self.interactions.append(Interaction(
            duration = "auto",
            content = Content(
                popup = 4,
                text = MText(text),
                voice = len(self.transcripts) - 1
            ),
            figure = -1 if narrator in VISIBLE_ACTORS else None,
            actorId = self._getUserId(narrator),
            type = "talk"
        ))

    def updateNarration(self, pos, text=None, narrator=None, alternativeText=None):
        transcript = text if isinstance(text, dict) else ({self.locale: text} if text != None else None)
        alternative = alternativeText if isinstance(alternativeText, dict) else ({self.locale: alternativeText} if alternativeText != None else None)
        if pos < len(self.transcripts) and pos >= 0 and (transcript!=None or narrator!=None or alternative!=None):
            self.transcripts[pos].reset2basename()
            if transcript != None:
                self.transcripts[pos].transcript = MText(self.transcripts[pos].transcript).merge(text)
                self.interactions[pos].content.text = MText(self.interactions[pos].content.text).merge(text)
            if alternative != None:
                self.transcripts[pos].alternative = MText(self.transcripts[pos].alternative).merge(text)
            if narrator != None:
                self.transcripts[pos].reset2basename(narrator)
                self.interactions[pos].actorId = self._getUserId(narrator)
                self.interactions[pos].figure = -1 if narrator in VISIBLE_ACTORS else None

    def removeNarration(self, pos):
        if pos < len(self.transcripts) and pos >= 0:
            self.transcripts.pop(pos)
            self.interactions.pop(pos)
            if pos < len(self.interactions):
                for i, interaction in enumerate(self.interactions[pos:]):
                    self.interactions[i].content.voice = interaction.content.voice - 1

    def __audible_script_list__(self):
        return [self.transcripts]

    def export(self, voiceOffset=0, pageId=0.0):
        outTranscripts = [transcript.export() \
                            for transcript in self.transcripts + self.mutescripts \
                            if transcript is not None and transcript.export() is not None]
        
        outInteractions = []
        for interaction in (self.defaultInteractions + self.interactions):
            newInteration = None
            if interaction.content.voice != None and interaction.content.voice > -1:
                newInteration = interaction.copy()
                newInteration.content.voice += voiceOffset
            exported = newInteration.export() if newInteration != None else interaction.export() 
            if exported != None:
                outInteractions.append(exported)

        eventDict = {
            "id": pageId,
            "scene": self.scene.export(),
            "board": self.board.export(),
            "objects": copy.deepcopy(self.objects),
            "interactions": outInteractions
        }

        if self.duration is not None:
            eventDict["duration"] = self.duration

        if self.transition is not None:
            eventDict["transition"] = self.transition

        return {
            "voices": outTranscripts,
            "events": [eventDict]
        }


##### 黑板页面 #####
class BoardPage(Page):
    def __init__(self, pageType, storyInstance, **kwargs):
        assert pageType in ("cover", "blackboard", "classroom")
        super().__init__(pageType, storyInstance)
        self.scene = Scene.load(self.story.styles["scenarios"][self.pageType])
        self.board = Board()
        self.narrations = {"transcripts": [], "interactions": []}
        self.narrator = self.story.narrator
        self.narratorId = -1
        self.boardContentScript = None
        self.boardContentListScripts = []
        self.defaultInteraction = None
        self.hasImage = False
        self.enableImageMagnify = True if self.pageType == "classroom" else False

        if all(key in kwargs for key in ("voices", "board", "objects", "interactions")):
            voices = kwargs.get("voices", None)
            self.scene = Scene.load(kwargs["scene"]) if kwargs.get("scene", None) != None else self.scene
            self.board = Board.load(kwargs.get("board", None))
            self.objects = kwargs.get("objects", None)
            if self.board.content.caption != None:
                self.boardContentScript = Script(transcript=self.board.content.caption)
            self.hasImage = True if (self.board.rect != None or self.board.content.rect != None or len(self.board.contentList) > 0) else False
            if self.objects != None:
                self.actor, self.actorId, self.narrator, self.narratorId, _, _ = get_actors(self.objects)

            if kwargs.get("interactions", None) != None:
                for interaction in kwargs["interactions"]:
                    if isinstance(interaction, dict):
                        # interactions that involves posters, or non visible-actor-involved
                        if "actor" in interaction and "content" in interaction \
                            and (("onResult" in interaction and (interaction["onResult"][0] if isinstance(interaction["onResult"], list) else interaction["onResult"]) > 0) \
                            or ("onPoster" in interaction and (interaction["onPoster"][0] if isinstance(interaction["onPoster"], list) else interaction["onPoster"]) > 0) \
                            or (self.objects[interaction["actor"]]["name"] not in VISIBLE_ACTORS)):
                            actorId = interaction["actor"]
                            content = interaction["content"]
                            if isinstance(content, dict) and "text" in content: # and "voice" in content and content["voice"] > 0:
                                text = content["text"]
                                voiceId = content.get("voice", -1)
                                self.narrations["transcripts"].append(Script(
                                    sound = voices[voiceId]["sound"] if voiceId > 0 else None,
                                    transcript = MText(text),
                                    narrator = self.objects[actorId]["name"],
                                    languages = voices[voiceId]["languages"] if (voiceId > 0 and "languages" in voices[voiceId] and isinstance(voices[voiceId]["languages"], list)) else None
                                ))
                                self.narrations["interactions"].append(Interaction(
                                    duration = interaction.get("duration", ""),
                                    actorId = actorId,
                                    figure = interaction.get("figure", None),
                                    content = Content(
                                        popup = 4,
                                        text = MText(text),
                                        voice = len(self.narrations["transcripts"]) - 1 if voiceId > 0 else voiceId
                                    ),
                                    onPoster = interaction.get("onResult", None) or interaction.get("onPoster", None),
                                    type = interaction.get("type", None)
                                ))
                        # visible-actor-involved interactions
                        elif "actor" in interaction:
                            actorId = interaction["actor"]
                            if "content" in interaction:
                                content = interaction["content"]
                                if isinstance(content, dict) and "text" in content: # and "voice" in content and content["voice"] > 0:
                                    text = content["text"]
                                    voiceId = content.get("voice", -1)
                                    self.transcripts.append(Script(
                                        sound=voices[voiceId]["sound"] if voiceId > 0 else None,
                                        transcript=MText(text),
                                        narrator=self.objects[actorId]["name"],
                                        languages=voices[voiceId]["languages"] if (voiceId > 0 and isinstance(voices[voiceId].get("languages", None), list)) else None
                                    ))
                                    self.interactions.append(Interaction(
                                        duration = interaction.get("duration", ""),
                                        content = Content(
                                            popup = content.get("popup", None),
                                            text = MText(text),
                                            voice = len(self.transcripts) - 1 if voiceId > 0 else voiceId
                                        ),
                                        actorId = actorId,
                                        type = interaction.get("type", None)
                                    ))
                            if ("figure" in interaction and interaction.get("figure", -1) > -1) and "position" in interaction:
                                self.defaultInteraction = Interaction(
                                    figure = interaction["figure"],
                                    position = interaction["position"],
                                    transform = interaction.get("transform", None),
                                    actorId = actorId,
                                    type = "talk"
                                )

    def updateActorPosition(self, oldPositions, newPositions):
        super().updateActorPosition(oldPositions, newPositions)
        if self.defaultInteraction!=None:
            currentPositionKey = None
            for key in oldPositions:
                if oldPositions[key] == self.defaultInteraction.position:
                    currentPositionKey = key
                    break
            if currentPositionKey in newPositions:
                self.defaultInteraction.position = newPositions[currentPositionKey]

    def updateActorTransform(self, oldTransform, newTransform):
        super().updateActorTransform(oldTransform, newTransform)
        if self.defaultInteraction != None and self.defaultInteraction.transform == oldTransform:
                self.defaultInteraction.transform = newTransform

    def setActor(self, actor, postures=["smilesay", "-stand-"], **kwargs):
        if actor in VISIBLE_ACTORS:
            if self.actor != actor:
                update_visible_actor(self.objects, actor)
                [script.reset2basename(actor) for script in self.transcripts]
                self.actor = actor

            posture_list = (
                [postures]
                if isinstance(postures, (str, int))
                else [postures[0]] \
                    if (isinstance(postures, list) and isinstance(postures[0], int))
                    else postures
            )
            figure, position = self.story.getUserPostureIdAndPosition(actor, posture_list, keyScenario="")
            if isinstance(kwargs.get("position", None), list) and len(kwargs["position"]) == 2:
                position = kwargs["position"]
            scale = None
            if isinstance(kwargs.get("scale", None), (int, float)) and kwargs["scale"] > 0:
                scale = f"scale({kwargs['scale']})"
            self.defaultInteraction = Interaction(
                                figure = figure,
                                position = position,
                                transform = scale if scale != None else self.story.styles["transform"],
                                type = "talk",
                                actorId = self._getUserId(actor)
                            )
        elif actor == None:
            self.defaultInteraction = None

    def setDialog(self, text:Union[str, dict], alternativeText:Union[str, dict]=None, **kwargs):
        newTranscript = Script(
            sound = switch_to_basename(self.transcripts[0].sound) \
                if (len(self.transcripts) > 0 and isinstance(self.transcripts[0], Script) \
                    and self.transcripts[0].sound != None and len(self.transcripts[0].sound) > 0) \
                else f"voice-{uuid.uuid4()}.mp3",
            transcript = MText(text),
            narrator = self.actor,
            languages = kwargs["languages"] if isinstance(kwargs.get("languages", None), list) else None,
            alternative = MText(alternativeText) if alternativeText != None else None
        )
            
        newInteraction = Interaction(
            duration = "",
            content = Content(
                popup = kwargs.get("popup", self.story.styles["popup"]),
                text = MText(text),
                voice = 0
            ),
            type = "talk",
            figure = -1, 
            actorId = self._getUserId(self.actor)
        )
        self.transcripts = [newTranscript] + self.transcripts[1:] if self.transcripts else [newTranscript]
        self.interactions = [newInteraction] + self.interactions[1:] if self.interactions else [newInteraction]

        if self.story._postureSelector != None and self.actor in ["boy", "girl"]:
            aiPosture = self.story._postureSelector.get_best_posture(
                    self.actor, 
                    text, 
                    self.story._defaultCharacters[self.actor][self.defaultInteraction.figure].split('-')[1]
                )[0]
            print(f"new posture is {aiPosture}")
            self.defaultInteraction.figure, _ = self.story.getUserPostureIdAndPosition(self.actor, aiPosture, keyScenario="")

    def addDialog(self, text:Union[str, dict], alternativeText:Union[str, dict]=None, **kwargs):
        self.transcripts.append(Script(
            sound = f"voice-{uuid.uuid4()}.mp3",
            transcript = MText(text),
            narrator = self.actor,
            languages = kwargs["languages"] if isinstance(kwargs.get("languages", None), list) else None,
            alternative = MText(alternativeText) if alternativeText != None else None
        ))

        self.interactions.append(Interaction(
            duration="auto",
            content = Content(
                popup=kwargs.get("popup", self.story.styles["popup"]),
                text=MText(text),
                voice=len(self.transcripts) - 1
            ),
            figure=-1,
            actorId=self._getUserId(self.actor),
            type="talk"))

    def updateDialog(self, pos, text:Union[str, dict]=None, alternativeText:Union[str, dict]=None, popup=None):
        if pos < len(self.transcripts) and pos >= 0:
            self.transcripts[pos].transcript = MText(self.transcripts[pos].transcript).merge(text)
            if alternativeText != None:
                self.transcripts[pos].alternative = MText(self.transcripts[pos].alternative).merge(alternativeText)
            self.transcripts[pos].reset2basename()

            self.interactions[pos].content.text = MText(self.interactions[pos].content.text).merge(text)
            if popup != None:
                self.interactions[pos].popup = popup

    def removeDialog(self, pos):
        if pos < len(self.transcripts) and pos >= 0:
            self.transcripts.pop(pos)
            self.interactions.pop(pos)
            if pos < len(self.interactions):
                for i, interaction in enumerate(self.interactions[pos:]):
                    self.interactions[i].content.voice = interaction.content.voice - 1

    def addNarration(self, text:Union[str, dict], narrator=None, alternativeText:Union[str, dict]=None, sound=None, **kwargs):
        narrator = self.pageType if kwargs.get("soundReady", None)==True \
            else (narrator if narrator != None else self.narrator if self.narrator != None else self.actor)

        newSound = os.path.basename(sound) if sound!=None else None
        if sound!=None and kwargs.get("soundReady", None)==True:
            try:
                self.story._cosUploader.local2cos(sound, self.story.storyId, self.story.audioPath)
                newSound = self.story.getAudioPath(os.path.basename(sound))
            except Exception as e:
                print(f"Upload sound file failed for [{sound}]\n", e)

        self.narrations["transcripts"].append(Script(
            sound = f"voice-{uuid.uuid4()}.mp3" if sound == None else newSound,
            transcript = MText(text),
            narrator = narrator,
            alternative = MText(alternativeText) if alternativeText!=None else None,
            languages = kwargs["languages"] if isinstance(kwargs.get("languages", None), list) else None,
            soundReady=bool(kwargs.get("soundReady", False))
        ))

        self.narrations["interactions"].append(Interaction(
            duration="auto",
            content = Content(
                popup = 4,
                text = MText(text),
                voice = len(self.narrations["transcripts"]) - 1
            ),
            figure = -1 if narrator in VISIBLE_ACTORS else None,
            actorId = self._getUserId(narrator),
            type = "talk"))

    def updateNarration(self, pos, text:Union[str, dict]=None, narrator=None, alternativeText:Union[str, dict]=None, sound=None, **kwargs):
        if pos < len(self.narrations["transcripts"]) and pos >= 0 \
            and (text!=None or narrator!=None or alternativeText!=None or (sound!=None and bool(kwargs.get("soundReady", False)))):

            newNarrator = narrator if narrator != None else self.objects[self.narrations["interactions"][pos].actorId]["name"]

            if text != None:
                self.narrations["transcripts"][pos].transcript = MText(self.narrations["transcripts"][pos].transcript).merge(text)
                self.narrations["interactions"][pos].content.text = MText(self.narrations["interactions"][pos].content.text).merge(text)
            if alternativeText != None:
                self.narrations["transcripts"][pos].alternative = MText(self.narrations["transcripts"][pos].alternative).merge(alternativeText)

            if sound!=None and bool(kwargs.get("soundReady", False)):
                self.narrations["transcripts"][pos].sound = os.path.basename(sound)
                try:
                    self.story._cosUploader.local2cos(sound, self.story.storyId, self.story.audioPath)
                except Exception as e:
                    self.narrations["transcripts"][pos].sound = self.story.getAudioPath(os.path.basename(sound))
                    print(f"Upload sound file failed for [{sound}]\n", e)
                self.narrations["transcripts"][pos].narrator = self.pageType
                self.narrations["transcripts"][pos].soundReady = True
                self.narrations["interactions"][pos].actorId = self._getUserId(self.pageType)
                self.narrations["interactions"][pos].figure = None
            else:
                if self.narrations["transcripts"][pos].soundReady:
                    self.narrations["transcripts"][pos].sound = f"voice-{uuid.uuid4()}.mp3"
                    self.narrations["transcripts"][pos].soundReady = False
                    newNarrator = narrator if narrator != None else self.narrator if self.narrator != None else self.actor
                else:
                    self.narrations["transcripts"][pos].reset2basename(narrator)
                    newNarrator = narrator if narrator != None else self.objects[self.narrations["interactions"][pos].actorId]["name"]
                self.narrations["transcripts"][pos].narrator = newNarrator
                self.narrations["interactions"][pos].actorId = self._getUserId(newNarrator)
                self.narrations["interactions"][pos].figure = -1 if newNarrator in VISIBLE_ACTORS else None

    def removeNarration(self, pos):
        if pos < len(self.narrations["transcripts"]) and pos >= 0:
            self.narrations["transcripts"].pop(pos)
            self.narrations["interactions"].pop(pos)
            if pos < len(self.narrations["interactions"]):
                for i, interaction in enumerate(self.narrations["interactions"][pos:]):
                    self.narrations["interactions"][i].content.voice = interaction.content.voice - 1

    def setImage(self, source:Union[str, dict], rect:list=[0.2, 0.2, 400, 400], autoFit:bool=True, uploadToCos:bool=True, **kwargs):
        assert isinstance(rect, list) and len(rect) >= 4
        mSource = MText(source) if source!=None else None
        mCaption = MText(kwargs.get("caption", self.board.content.caption if self.board.content.caption != None else ""))
        if kwargs.get("sourceType", None) != "video" and mSource!=None:
            validUrl = False
            if is_valid_http_url(mSource.firstValidPair()[1]):
                width = rect[2]
                height = rect[3]
                validUrl = True
            else:
                width, height = get_image_size(mSource.firstValidPair()[1])
            assert width > 0 and height > 0

            if not validUrl:
                if autoFit:
                    rect = Page.fit_image_rect(rect, width, height)

                if uploadToCos:
                    if isinstance(mSource.data, dict):
                        for key in mSource.data:
                            mSource.data[key] = self.story.uploadImageToCos(mSource.data[key], applyHash=kwargs.get("applyHash", True))
                    else:
                        mSource.data = self.story.uploadImageToCos(mSource.data, applyHash=kwargs.get("applyHash", True))

        self.board = Board(
            content = Content(
                caption = mCaption,
                image = mSource if kwargs.get("sourceType", None) != "video" else None,
                src = mSource if kwargs.get("sourceType", None) == "video" else None,
                videoType = kwargs.get("videoType", None) if kwargs.get("sourceType", None) == "video" else None,
                fontSize = kwargs.get("fontSize", "24px") if mCaption.len() > 0 else None,
                fontColor = kwargs.get("fontSize", "white") if mCaption.len() > 0 else None,
                magnify = kwargs.get("magnify", self.enableImageMagnify),
                border = kwargs.get("borderStyle", self.story.styles["frame"]) if kwargs.get("border", self.enableImageMagnify) else None
            ),
            rect = rect
        )

        self.boardContentScript = Script(transcript=mCaption)
        self.hasImage = True

    def setVideo(self, source:Union[str, dict], autoFit:bool=True, rect:list=[0.1, 0.1, 640, 360], **kwargs):
        self.setImage(source=source, rect=rect, autoFit=autoFit, uploadToCos=False, sourceType="video", **kwargs)

    def addImage(self, source:Union[str, dict], rect:list=[0, 0, 1, 1], autoFit:bool=True, uploadToCos:bool=True, **kwargs):
        assert isinstance(rect, list) and len(rect) >= 4 and source!=None
        validUrl = False
        if is_valid_http_url(MText(source).firstValidPair()[1]):
            width = rect[2]
            height = rect[3]
            validUrl = True
        else:
            width, height = get_image_size(MText(source).firstValidPair()[1])
        assert width > 0 and height > 0
        mSource = MText(source) if source!=None else None
        mCaption = MText(kwargs.get("caption", ""))

        if not validUrl:
            if autoFit:
                rect = Page.fit_image_rect(rect, width, height)

            if uploadToCos:
                if isinstance(mSource.data, dict):
                    for key in mSource.data:
                        mSource.data[key] = self.story.uploadImageToCos(mSource.data[key], applyHash=kwargs.get("applyHash", True))
                else:
                    mSource.data = self.story.uploadImageToCos(mSource.data, applyHash=kwargs.get("applyHash", True))

        self.board.contentList.append(Content(
            caption = mCaption,
            image = mSource,
            rect = rect,
            fontSize = kwargs.get("fontSize", "24px") if mCaption.len() > 0 else None,
            fontColor = kwargs.get("fontSize", "white") if mCaption.len() > 0 else None,
            magnify = kwargs.get("magnify", self.enableImageMagnify),
            border = kwargs.get("borderStyle", self.story.styles["frame"]) \
                if kwargs.get("border", self.enableImageMagnify) \
                else None
            )
        )
        self.boardContentListScripts.append(Script(transcript=mCaption))

    def updateImage(self, pos:int, source:MText, rect:list=[0, 0, 1, 1], autoFit=True, uploadToCos=True, **kwargs):
        if pos < len(self.board.contentList) and pos >= 0:
            assert isinstance(rect, list) and len(rect) >= 4
            validUrl = False
            if is_valid_http_url(MText(source).firstValidPair()[1]):
                width = rect[2]
                height = rect[3]
                validUrl = True
            else:
                width, height = get_image_size(MText(source).firstValidPair()[1])
            assert width > 0 and height > 0
            mSource = MText(source) if source!=None else None
            mCaption = MText(kwargs.get("caption", \
                                        self.board.contentList[pos].caption \
                                            if self.board.contentList[pos].caption != None \
                                            else ""
                                        )
                            )
            if isinstance(self.board.contentList[pos].caption, MText):
                mCaption = self.board.contentList[pos].caption.merge(mCaption)

            if not validUrl:
                if autoFit:
                    rect = Page.fit_image_rect(rect, width, height)

                if uploadToCos:
                    if isinstance(mSource.data, dict):
                        for key in mSource.data:
                            mSource.data[key] = self.story.uploadImageToCos(mSource.data[key], applyHash=kwargs.get("applyHash", True))
                    else:
                        mSource.data = self.story.uploadImageToCos(mSource.data, applyHash=kwargs.get("applyHash", True))

            self.board.contentList[pos].image = self.board.contentList[pos].image.merge(mSource)
            self.board.contentList[pos].rect = rect
            self.board.contentList[pos].caption = mCaption
            self.board.contentList[pos].magnify = True if kwargs.get("magnify", self.enableImageMagnify) else False
            self.board.contentList[pos].border = kwargs.get("borderStyle", self.story.styles["frame"]) \
                if kwargs.get("border", self.enableImageMagnify) \
                else None

            self.boardContentListScripts[pos].transcript = mCaption

    def removeImage(self, pos:int):
        if pos < len(self.board.contentList) and pos >= 0:
            self.board.contentList.pop(pos)
            self.boardContentListScripts.pop(pos)

    def __audible_script_list__(self):
        return [self.transcripts, self.narrations["transcripts"]]

    def export(self, voiceOffset=0, pageId=0.0):
        outTranscripts = [transcript.export() for transcript in self.transcripts \
                         if isinstance(transcript, Script) and transcript.export() is not None]
        # only count those transcript-with-voice
        narrationOffset = len(outTranscripts)
        outTranscripts += [transcript.export() for transcript in (self.narrations["transcripts"] \
                            + [self.boardContentScript] + self.boardContentListScripts) \
                         if (isinstance(transcript, Script) and transcript.export() is not None)]

        tempInteractions = []
        if len(self.interactions) > 0:
            for interaction in self.interactions:
                updatedInteraction = interaction.merge(self.defaultInteraction) if self.defaultInteraction != None else interaction.copy()
                if self.hasImage:
                    updatedInteraction.content.popup = 4
                tempInteractions.append(updatedInteraction)
        else:
            if self.defaultInteraction != None:
                defaultInteraction = self.defaultInteraction.copy()
                defaultInteraction.type = "motion"
                tempInteractions.append(defaultInteraction)


        for interaction in self.narrations["interactions"]:
            tempNarration = interaction.copy()
            tempNarration.content.voice += narrationOffset
            tempInteractions.append(tempNarration)

        outInteractions = []
        for interaction in tempInteractions:
            if interaction.content.voice != None and interaction.content.voice > -1:
                interaction.content.voice += voiceOffset
            exported = interaction.export()
            if exported != None:
                outInteractions.append(exported)

        eventDict = {
            "id": pageId,
            "scene": self.scene.export(),
            "board": self.board.export(),
            "objects": copy.deepcopy(self.objects),
            "interactions": outInteractions
        }

        if self.duration is not None:
            eventDict["duration"] = self.duration

        if self.transition is not None:
            eventDict["transition"] = self.transition

        return {
            "voices": outTranscripts,
            "events": [eventDict]
        }


##### 黑板页面 #####
class BlackboardPage(BoardPage):
    def __init__(self, storyInstance, **kwargs):
        super().__init__("blackboard", storyInstance, **kwargs)

        if len(kwargs.get("source", "")) > 0:
            self.setImage(**kwargs)

        if kwargs.get("actor", -1) in VISIBLE_ACTORS:
            self.setActor(**kwargs)

    def addNarration(self, text, narrator=None, alternativeText=None, sound=None, **kwargs):
        super().addNarration(text, narrator, alternativeText, sound, **kwargs)
        if kwargs.get("onPoster", None) != None or kwargs.get("onResult", None) != None:
            onPosterId = kwargs.get("onPoster", None) or kwargs.get("onResult", None)
            if onPosterId > len(self.board.contentList) + (1): # onResult=1 is always reserved for board image
                print(f"{YELLOW}Warning{RESET}: onPoster/onResult is greater than available image count and is ignored.")
            else:
                self.narrations["interactions"][-1].onPoster = onPosterId

    def updateNarration(self, pos, text=None, narrator=None, alternativeText=None, sound=None, **kwargs):
        super().updateNarration(pos, text, narrator, alternativeText, sound, **kwargs)
        if kwargs.get("onPoster", None) != None or kwargs.get("onResult", None) != None:
            onPosterId = kwargs.get("onPoster", None) or kwargs.get("onResult", None)
            if onPosterId > len(self.board.contentList) + (1): # onResult=1 is always reserved for board image
                print(f"{YELLOW}Warning{RESET}: onPoster/onResult is greater than available image count and is ignored.")
            self.narrations["interactions"][pos].onResult = None
            self.narrations["interactions"][pos].onPoster = onPosterId
        elif "onPoster" in kwargs or "onResult" in kwargs:
            self.narrations["interactions"][pos].onPoster = None
            self.narrations["interactions"][pos].onResult = None


##### 封面页面 #####
class CoverPage(BoardPage):
    def __init__(self, storyInstance, **kwargs):
        super().__init__("cover", storyInstance, **kwargs)

        if kwargs.get("source", None) != None and len(kwargs["source"]) > 0:
            self.setImage(**kwargs)

    def setActor(self, **kwargs):
        pass
    
    def addDialog(self, **kwargs):
        pass

    def updateDialog(self, **kwargs):
        pass
    
    def removeDialog(self, **kwargs):
        pass


##### 教室页面 #####
class ClassroomPage(BoardPage):
    def __init__(self, storyInstance, **kwargs):
        super().__init__("classroom", storyInstance, **kwargs)

        if "actor" in kwargs and kwargs["actor"] in VISIBLE_ACTORS:
            self.setActor(**kwargs)
    
    def addNarration(self, text, narrator=None, alternativeText=None, sound=None, **kwargs):
        super().addNarration(text, narrator, alternativeText, sound, **kwargs)
        if kwargs.get("onPoster", None) != None or kwargs.get("onResult", None) != None:
            onPosterId = kwargs.get("onPoster", None) or kwargs.get("onResult", None)
            if onPosterId > len(self.board.contentList) + (1): # onResult=1 is always reserved for board image
                print(f"{YELLOW}Warning{RESET}: onPoster/onResult is greater than available image count and is ignored.")
            else:
                self.narrations["interactions"][-1].onPoster = onPosterId

    def updateNarration(self, pos, text=None, narrator=None, alternativeText=None, sound=None, **kwargs):
        super().updateNarration(pos, text, narrator, alternativeText, sound, **kwargs)
        if kwargs.get("onPoster", None) != None or kwargs.get("onResult", None) != None:
            onPosterId = kwargs.get("onPoster", None) or kwargs.get("onResult", None)
            if onPosterId > len(self.board.contentList) + (1): # onResult=1 is always reserved for board image
                print(f"{YELLOW}Warning{RESET}: onPoster/onResult is greater than available image count and is ignored.")
            self.narrations["interactions"][pos].onResult = None
            self.narrations["interactions"][pos].onPoster = onPosterId
        elif "onPoster" in kwargs or "onResult" in kwargs:
            self.narrations["interactions"][pos].onPoster = None
            self.narrations["interactions"][pos].onResult = None