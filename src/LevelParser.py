
class LevelParser:
    '''
    parses .level file and returns matrix of entity ids
    '''
    @classmethod
    def load_level(self, path):
        if path[-6:] != '.level': raise ValueError('Incorrect file type for level (requires .level)')
        matrix = list()
        try:
            level_file = open(path, 'r')
        except:
            raise FileNotFoundError(f'Cannot open level file {path} ... check path')
        for line in level_file.readlines():
            line = line.rstrip()
            matrix.append([int(c) for c in line])
        return matrix

level_01 = LevelParser.load_level('../levels/1-01.level')
