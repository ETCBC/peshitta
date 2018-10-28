import os
import collections
import operator
import re
from functools import reduce
from shutil import rmtree
from tf.transcription import Transcription
from tf.fabric import Fabric


VERSION = '0.1'

GH_BASE = os.path.expanduser('~/github')
ORG = 'etcbc'
REPO = 'peshitta'
SOURCE_DIR = f'source/{VERSION}'
PLAIN_DIR = f'plain/{VERSION}'
TF_DIR = f'tf/{VERSION}'
SOURCE_PATH = f'{GH_BASE}/{ORG}/{REPO}/{SOURCE_DIR}'
PLAIN_PATH = f'{GH_BASE}/{ORG}/{REPO}/{PLAIN_DIR}'
TF_PATH = f'{GH_BASE}/{ORG}/{REPO}/{TF_DIR}'

TR = Transcription()


allAcrosSeq = '''
    Gn
    Ex
    Lv
    Nm
    Dt
    Jb
    Jos
    Jd
    Sm1
    Sm2
    Ps
    Rg1
    Rg2
    Pr
    Sap
    Ec
    Ct
    Is
    Jr
    Thr
    EpJr
    EpBar_A
    EpBar_B
    Bar
    Ez
    Hs
    Jl
    Am
    Ob
    Jon
    Mi
    Na
    Hb
    Zf
    Hg
    Sa
    Ml
    Dn
    BelDr
    Ru
    Sus
    Est
    Jdt
    Sir
    Chr1
    Chr2
    ApBar
    Esr4
    Ezr
    Neh
    Mc1_A
    Mc1_B
    Mc2
    Mc3
    Mc4
    Oda
    OrM_A
    OrM_B
    ApcPs_A
    ApcPs_B
    ApcPs
    PsS
    Tb_A
    Tb_B
    Esr3
'''.strip().split()

allAcros = set(allAcrosSeq)

commonMetaData = collections.OrderedDict(
    dataset=REPO,
    datasetName='Peshitta',
    source='SEDRA',
    sourceUrl='https://sedra.bethmardutho.org/about/contributors',
    encoders=(
        'Eep Talstra Centre for Bible and Computer. '
        'LinkSyr project (CLARIAH research pilot). '
        'Hannes Vlaardingerbroek, Constantijn Sikkel (PIL) '
        'and Dirk Roorda (TF)'),
    email1='dirk.roorda@dans.knaw.nl',
)
specificMetaData = collections.OrderedDict(
    book='book name',
    acro='book acronym',
    witness='book witness (A or B)',
    chapter='chapter number',
    verse='verse number',
    word='full form of the word in syriac script',
    trailer='after-word material in syriac script',
    word_etcbc='full form of the word in ETCBC transcription',
    trailer_etcbc='after-word material in ETCBC transcription',
)
langMetaData = dict(
    en=dict(
        language='English',
        languageCode='en',
        languageEnglish='English',
    ),
)
numFeatures = set(
    '''
    chapter
    verse
'''.strip().split()
)

oText = {
    'sectionFeatures': 'book,chapter,verse',
    'sectionTypes': 'book,chapter,verse',
    'fmt:text-orig-full': '{word}{trailer}',
    'fmt:text-trans-full': '{word_etcbc}{trailer_etcbc}',
}

SPLIT_PAT = r'(.*?)({})(.*)'.format('|'.join(re.escape(p) for p in TR.syriac_punctuation_trans))
SPLIT_RE = re.compile(SPLIT_PAT)


def splitWord(word):
  match = SPLIT_RE.fullmatch(word)
  if not match:
    return [[word, ' ']]
  (word, punct, rest) = match.groups()
  result = [[word, punct + ' ']]
  if len(rest):
    result.extend(splitWord(rest))
  return result


def splitWords(words):
  resultWords = []
  for word in words:
    for (w, p) in splitWord(word):
      if w == '' and len(resultWords):
        resultWords[-1][1] += f' {p}'
      else:
        resultWords.append([w, p])
  return resultWords or [['', '']]


def doText(book, chapter, verse, text, results, content):
  words = text.strip().split()
  results['problems'] |= {word for word in words if not TR.can_to_syriac(word)}
  results['chars'] |= set(''.join(words))
  content.setdefault(book, {}).setdefault(int(chapter), {})[int(verse)] = text.strip()


def doBooks():
  bookInfo = {}
  bookAcro = {}
  content = {}

  print('Parsing book files')

  with os.scandir(SOURCE_PATH) as bookDir:
    for bookEntry in bookDir:
      if not bookEntry.is_file():
        continue
      bookFile = bookEntry.name
      bookMain = bookFile[0:-2] if bookFile[-2] == '_' else bookFile
      bookAb = bookFile[-1] if bookFile[-2] == '_' else ''
      bookAbRep = '' if bookAb == '' else f'_{bookAb.upper()}'
      bookMain = f'{bookMain[1:]}_{bookMain[0]}' if bookMain[0].isdigit() else bookMain
      bookName = f'{bookMain}{bookAbRep}'
      bookExtra = '' if bookName == bookFile else f' => {bookName}'
      print(f'{bookFile:<20}{bookExtra}')
      thisBookInfo = {'bookName': bookName}
      if bookAb:
        thisBookInfo['witness'] = bookAb
      results = dict(chars=set(), problems=set())
      with open(f'{SOURCE_PATH}/{bookFile}') as bh:
        (curChapter, curVerse, curText) = (None, None, None)
        for line in bh:
          if line.startswith('%'):
            comps = line[1:-1].split()
            if len(comps) == 0:
              continue
            keyword = comps[0]
            args = comps[1:]
            if keyword == 'bookname':
              acro = ' '.join(args)
              acro = f'{acro[1:]}{acro[0]}' if acro[0].isdigit() else acro
              bookAbRep = '' if bookAb == '' else f'_{bookAb.upper()}'
              thisBookInfo['acro'] = f'{acro}{bookAbRep}'
            elif keyword == 'language':
              thisBookInfo['language'] = ' '.join(args)
            elif keyword == 'verse':
              if curVerse:
                doText(bookName, curChapter, curVerse, curText, results, content)
              (curChapter, curVerse) = args[0].split(',')
              curText = ''
          elif curVerse:
            curText += line
        if curVerse:
          doText(bookName, curChapter, curVerse, curText, results, content)
      thisBookInfo['problems'] = sorted(results['problems'])
      thisBookInfo['chars'] = ''.join(sorted(results['chars']))
      bookInfo[bookName] = thisBookInfo
      bookAcro[thisBookInfo['acro']] = thisBookInfo
  return (bookInfo, bookAcro, content)


def checks(allAcros, bookInfo):
  allChars = set()
  for thisBookInfo in bookInfo.values():
    allChars |= set(thisBookInfo['chars'])

  sortedChars = ''.join(sorted(allChars))

  print(f'ALL CHARS = {sortedChars}')

  transcriptionProblems = 0

  for (book, thisBookInfo) in sorted(bookInfo.items()):
    acro = thisBookInfo['acro']
    lang = thisBookInfo['language']
    chars = thisBookInfo['chars']
    problems = thisBookInfo['problems']
    if problems:
      print(f'{acro:<5} = {book:<20} in {lang:<7} having {chars}')
      transcriptionProblems += len(problems)
      print(f'\tPROBLEMS: {" ".join(problems)}')

  print(
      f'XX: {transcriptionProblems} transcription problems'
      if transcriptionProblems else
      'OK: Transcription'
  )
  # books
  allDeclared = True
  allCorpus = set()
  for (book, thisBookInfo) in sorted(bookInfo.items()):
    acro = thisBookInfo['acro']
    allCorpus.add(acro)
    if acro not in allAcros:
      allDeclared = False
      print(f'CORPUS: book {book} = {acro} not in declared list')
  print('CORPUS: ' + ('OK: all books declared' if allDeclared else 'XX: some undeclared books'))
  allInCorpus = True
  for acro in sorted(allAcros):
    if acro not in allCorpus:
      allInCorpus = False
      print(f'DECLARED: {acro} not in corpus')
  print('DECLARED: ' + ('OK: all books in corpus' if allInCorpus else 'XX: some missing books'))


def writeUnicode(content):
  if os.path.exists(PLAIN_PATH):
    rmtree(PLAIN_PATH)
  os.makedirs(PLAIN_PATH, exist_ok=True)
  for (book, chapters) in content.items():
    with open(f'{PLAIN_PATH}/{book}.txt', 'w') as fh:
      for (chapter, verses) in sorted(chapters.items()):
        fh.write(f'Chapter {chapter}\n\n')
        for (verse, text) in sorted(verses.items()):
          sycText = TR.to_syriac(text)
          fh.write(f'{verse} {sycText}\n')
        fh.write('\n')


def generateTf(bookAcro, content):
  if os.path.exists(TF_PATH):
    rmtree(TF_PATH)
  os.makedirs(TF_PATH)

  print('Slicing content into features')

  cur = collections.Counter()
  curSlot = 0
  context = []
  nodeFeatures = collections.defaultdict(dict)
  edgeFeatures = collections.defaultdict(
      lambda: collections.defaultdict(set)
  )
  oSlots = collections.defaultdict(set)
  for acro in allAcrosSeq:
    thisBookInfo = bookAcro[acro]
    bookName = thisBookInfo['bookName']
    witness = thisBookInfo.get('witness', None)
    chapters = content[bookName]

    cur['book'] += 1
    bookNode = ('book', cur['book'])
    nodeFeatures['book'][bookNode] = acro
    nodeFeatures['book@en'][bookNode] = bookName
    if witness is not None:
      nodeFeatures['witness'][bookNode] = witness
    context.append(('book', cur['book']))

    for chapterNum in chapters:
      verses = chapters[chapterNum]

      cur['chapter'] += 1
      nodeFeatures['chapter'][('chapter', cur['chapter'])] = chapterNum
      nodeFeatures['book'][('chapter', cur['chapter'])] = acro
      if witness is not None:
        nodeFeatures['witness'][('chapter', cur['chapter'])] = witness
      context.append(('chapter', cur['chapter']))

      for verseNum in verses:
        words = verses[verseNum].strip().split()

        cur['verse'] += 1
        nodeFeatures['verse'][('verse', cur['verse'])] = verseNum
        nodeFeatures['chapter'][('verse', cur['verse'])] = chapterNum
        nodeFeatures['book'][('verse', cur['verse'])] = acro
        if witness is not None:
          nodeFeatures['witness'][('verse', cur['verse'])] = witness
        context.append(('verse', cur['verse']))
        for elem in splitWords(words):
          if len(elem) != 2:
            print(bookName, chapterNum, verseNum, words)
            continue
          (word, punc) = elem
          wSyc = TR.to_syriac(word)
          pSyc = TR.to_syriac(punc)

          curSlot += 1
          wordNode = ('word', curSlot)
          nodeFeatures['word_etcbc'][wordNode] = word
          nodeFeatures['word'][wordNode] = wSyc
          nodeFeatures['trailer_etcbc'][wordNode] = punc
          nodeFeatures['trailer'][wordNode] = pSyc
          for (nt, curNode) in context:
            oSlots[(nt, curNode)].add(curSlot)
        context.pop()
      context.pop()
    context.pop()

  if len(context):
      print('Context:', context)

  print(f'\n{curSlot:>7} x slot')
  for (nodeType, amount) in sorted(cur.items(), key=lambda x: (x[1], x[0])):
      print(f'{amount:>7} x {nodeType}')

  nValues = reduce(
      operator.add, (len(values) for values in nodeFeatures.values()), 0
  )
  print(f'{len(nodeFeatures)} node features with {nValues} values')
  print(f'{len(oSlots)} nodes linked to slots')

  print('Compiling TF data')
  print(f'Building warp feature otype')

  nodeOffset = {'word': 0}
  oType = {}
  n = 1
  for k in range(n, curSlot + 1):
      oType[k] = 'word'
  n = curSlot + 1
  for (nodeType, amount) in sorted(cur.items(), key=lambda x: (x[1], x[0])):
      nodeOffset[nodeType] = n - 1
      for k in range(n, n + amount):
          oType[k] = nodeType
      n = n + amount
  print(f'{len(oType)} nodes')

  print('Filling in the nodes for features')

  newNodeFeatures = collections.defaultdict(dict)
  for (ft, featureData) in nodeFeatures.items():
      newFeatureData = {}
      for ((nodeType, node), value) in featureData.items():
          newFeatureData[nodeOffset[nodeType] + node] = value
      newNodeFeatures[ft] = newFeatureData
  newOslots = {}
  for ((nodeType, node), slots) in oSlots.items():
      newOslots[nodeOffset[nodeType] + node] = slots

  nodeFeatures = newNodeFeatures
  nodeFeatures['otype'] = oType
  edgeFeatures['oslots'] = newOslots

  print(f'Node features: {" ".join(nodeFeatures)}')
  print(f'Edge features: {" ".join(edgeFeatures)}')

  metaData = {
      '': commonMetaData,
      'otext': oText,
      'oslots': dict(valueType='str'),
      'book@en': langMetaData['en'],
  }
  for ft in set(nodeFeatures) | set(edgeFeatures):
      metaData.setdefault(
          ft, {}
      )['valueType'] = 'int' if ft in numFeatures else 'str'
      metaData[ft]['description'] = (
          specificMetaData[ft] if ft in specificMetaData else '?'
      )

  TF = Fabric(locations=TF_PATH, silent=True)
  TF.save(
      nodeFeatures=nodeFeatures,
      edgeFeatures=edgeFeatures,
      metaData=metaData
  )


(bookInfo, bookAcro, content) = doBooks()

checks(allAcros, bookInfo)
writeUnicode(content)
generateTf(bookAcro, content)
