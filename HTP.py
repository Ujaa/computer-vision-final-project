class HTP:
  def __init__(self, detected_result):
    self.detected_result = detected_result
    self.results = {
      'keywords': set(),
      'house': '집은 자신의 가정 생활과 가족 관계를 어떻게 인지하는지, 어떠한 감정을 갖고 있는지 알 수 있으며, 자신이 바라보는 현재의 가정의 모습, 과거의 가정의 모습, 그리고 이상적인 장래에 대한 소망을 나타냅니다.',
      'tree': '나무 그림은 자신의 개인적인 변화 과정을 나타내며, 나무의 아래에서 위로 갈수록 최근의 경험을 나타내는 경향이 있습니다.',
      'person': '자신의 자아상과 자신이 바라보는 자신의 중요한 주위 사람들에 대한 상을 나타냅니다.'
    }
    self.house_classes = ['door', 'sun', 'grass', 'fence', 'window']
    self.tree_classes = ['fruit', 'bird', 'flower', 'leaf', 'branch', 'trunk']
    self.person_classes = ['ear', 'nose', 'mouth', 'arm', 'eye']
    self.classes_HTP = {
      'house': [],
      'tree': [],
      'person': [],
    }
    self.classes = {
      'door': {
        'coords': [],
        'count': 0,
        'threshold': 1,
        'up': '개방적',
        'down': '은둔적',
      },
      'sun': {
        'coords': [],
        'count': 0,
        'threshold': 1,
        'up': '의존적',
        'down': '자립적',
      },
      'grass': {
        'coords': [],
        'count': 0,
      },
      'fence': {
        'coords': [],
        'count': 0,
        'threshold': 1,
        'up': '방어적',
        'down': '개방적',
      },
      'window': {
        'coords': [],
        'count': 0,
        'threshold': 3,
        'up': '개방적',
        'down': '방어적',
      },
      'fruit': {
        'coords': [],
        'count': 0,
        'threshold': 3,
        'up': '애정욕구',
        'down': '자립적',
      },
      'bird': {
        'coords': [],
        'count': 0,
        'threshold': 3,
        'up': '안정감 부족',
        'down': '안정적',
      },
      'flower': {
        'coords': [],
        'count': 0,
      },
      'leaf': {
        'coords': [],
        'count': 0,
      },
      'branch': {
        'coords': [],
        'count': 0,
      },
      'trunk': {
        'coords': [],
        'count': 0,
      },
      'ear': {
        'coords': [],
        'count': 0,
        'threshold': 2,
        'up': '자립적',
        'down': '두려움',
      },
      'nose': {
        'coords': [],
        'count': 0,
        'threshold': 1,
        'up': '안정적',
        'down': '위축감',
      },
      'mouth': {
        'coords': [],
        'count': 0,
        'threshold': 1,
        'up': '안정적',
        'down': '의사소통 거부',
      },
      'arm': {
        'coords': [],
        'count': 0,
        'threshold': 2,
        'up': '안정적',
        'down': '죄의식',
      },
      'eye': {
        'coords': [],
        'count': 0,
        'threshold': 2,
        'up': '안정적',
        'down': '소극적',
      },
    }

    

  def calculate_area(self, x1, y1, x2, y2):
      width = abs(x2 - x1)
      height = abs(y2 - y1)

      area = width * height

      return area

  def get_house_analysis(self, name, info):
    if(name == 'door'):
      if (info['count'] == 0):
        return " 가정환경에서 타인과 접촉하지 않으려는 감정을 가지고 있고, 외부세계와의 교류를 원치 않는 편입니다."
      else:
        return " 타인에 대한 의존심을 보입니다."
    elif(name == 'window'):
      if (info['count'] == 0):
        return " 철회와 상당한 편집증적 경향성을 보이고 있습니다."
      elif(info['count'] >= 3):
        return " 개방과 환경적 접촉에 대한 갈망을 가지고 있습니다."
    elif(name == 'fence'):
      if (info['count'] != 0):
        return " 방어적이고, 안전을 방해받고 싶어하지 않습니다."
    elif(name == 'grass'):
      if (info['count'] >= 4):
        return " 타인과 상호작용에 거리를 두기는 하지만 나중에 신뢰감을 형성하고 경계를 허물게 되면 친밀감을 잘 쌓을 수 있습니다."
    return None

  def get_tree_analysis(self, name, info):
    tree_x1, tree_y1, tree_x2, tree_y2 = self.classes_HTP['tree']

    if(name == 'fruit'):
      if (info['count'] >= 3):
        return ' 사랑과 관심을 받고 싶거나 사랑을 주고 싶어하는 욕구가 있습니다. 또는, 감정적인 충족, 만족, 즐거움을 나타낼 수 있습니다.'
      elif (info['count'] == 0):
        return ' 감정적으로 불만족스러운 경험이나 성장의 어려움을 나타낼 수 있습니다.'
    elif(name == 'flower'):
      if (info['count'] != 0):
        return ' 주변에서 든든함을 얻을 수 있는 매개체가 있으며, 체면 겉치레를 중요시하거나 자신을 찬미합니다.'
    elif(name == 'leaf'):
      if (info['count'] == 0):
        return ' 내성적이거나 감정적으로 억압된 느낌을 나타낼 수 있습니다.'
      else: 
        max_y, min_y = 0 , 10000
        for coord in info['coords']:
          y1, y2 = coord[1], coord[3]
          if max_y < y2:
            max_y = y2
          if min_y > y1:
            min_y = y1

        tree_height = abs(tree_y2 - tree_y1)/2
        leaf_height = abs(max_y - min_y)/2
        print(tree_height, leaf_height)

        if tree_height < leaf_height:
          return ' 사회적 요구에 순응할 수 없거나 유연하게 적응할 능력이 부족한 느낌입니다.'
        else:
          if (info['count'] >= 3):
            return ' 창의적이며 호기심이 많은 성격일 수 있습니다.'
    elif(name == 'branch'):
      if (info['count'] >= 3):
        return ' 개방적이고 활동적인 성향, 다양한 관심사 및 활동을 가진 성격일 수 있습니다'
      elif (info['count'] == 0):
        return ' 대인 관계나 활동적인 측면에서 부족함을 나타낼 수 있습니다. 소통에 어려움을 겪거나, 다양한 경험을 쌓기 어려운 상황을 나타낼 수 있습니다.'
    elif(name == 'trunk'):
      if (info['count'] != 0):
        trunk_x1, trunk_y1, trunk_x2, trunk_y2 = info['coords'][0]

        tree_width = abs(tree_x2 - tree_x1)
        trunk_width = abs(trunk_x2 - trunk_x1)

        if trunk_width >= 0.6 * tree_width:
          print("강인하고 안정된 성격을 나타낼 수 있습니다. 자기 자신에 대한 확신이 있거나, 안정된 가정이나 기반을 갖추고 있다는 것을 나타낼 수 있습니다.")
        else:
          print("자아의 불안정성, 자기보호 메커니즘의 부재, 또는 정체성에 대한 불확실성을 나타낼 수 있습니다.")
    return None

  def get_person_analysis(self, name, info):
    if(name == 'ear'):
      if (info['count'] == 0):
        return ' 귀는 타인으로부터 정보를 받아들이는 통로입니다. 정서적 교류나 감정표현에 대해 불안하고 자신감이 부족합니다.'
    elif(name == 'nose'):
      if (info['count'] == 0):
        return ' 코는 환경으로부터 정서적 자극을 어떻게 받아들이는지 알 수 있습니다. 성에 대해 무엇인가 갈등이 있으며 타인에게 어떻게 보일지에 매우 예민하고 두려워합니다.'
    elif(name == 'mouth'):
      if (info['count'] == 0):
        return ' 입은 심리적으로 충족 여부를 알 수 있습니다. 애정 욕구의 강한 거부, 심한 죄의식, 우울감이 있으며, 부모와 같은 대상과의 관계에 상당한 갈등이나 결핍이 있습니다.'
    elif(name == 'arm'):
      if (info['count'] == 0):
        return ' 팔은 자아 발달과 환경과의 접촉, 대인관계, 사회적 적응을 나타내며, 죄의식, 일반적인 무력감, 환경에 대한 불만이 나타납니다.'
    elif(name == 'eye'):
      if (info['count'] == 0):
        return ' 눈은 세상을 향한 창문입니다. 타인과 감정을 교류하는데 극심한 불안감을 느끼거나 사고장애의 가능성을 가지고 있습니다.'
      elif (info['count'] == 1):
        return ' 눈은 세상을 향한 창문입니다. 감정교류에 있어서 접근과 회피의 양가감정을 가지고 있습니다.'
      elif (info['count'] == 2):
        return ' 눈은 세상을 향한 창문입니다. 타인과 정상 범위의 정서적 교류가 가능합니다.'
    return None

  def get_result(self):
    for result in self.detected_result:
      
      class_name = result['name']
      x1, y1, x2, y2 = int(result['xmin']), int(result['ymin']), int(result['xmax']), int(result['ymax'])

      if (class_name in self.classes_HTP):
        self.classes_HTP[class_name] = [x1, y1, x2, y2]

      if (class_name in self.classes):
        self.classes[class_name]['count'] += 1
        self.classes[class_name]['coords'].append([x1, y1, x2, y2])
    
    for name, info in self.classes.items():
      # 키워드 추가하기
      if 'threshold' in info:
        if info['count'] >= info['threshold']:
          self.results['keywords'].add(info['up'])
        else:
          self.results['keywords'].add(info['down'])

      # 설명 추가하기
      if(name in self.house_classes):
        if(self.get_house_analysis(name, info) is not None): self.results['house'] += self.get_house_analysis(name, info)
      elif(name in self.tree_classes):
        if(self.get_tree_analysis(name, info) is not None): self.results['tree'] += self.get_tree_analysis(name, info)
      elif(name in self.person_classes):
        if(self.get_person_analysis(name, info) is not None): self.results['person'] += self.get_person_analysis(name, info)
    
    self.results['keywords'] = sorted(self.results['keywords'])
    return self.results

