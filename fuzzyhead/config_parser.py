import configparser

parser=configparser.ConfigParser()
parser.read_file(open('config', 'r'))
global registry
global dict_source
global dict_upload
global dict_remove
global backend
global broker
registry=parser.get('URLs', 'registry')
dict_source=parser.get('URLs', 'dict_source')
dict_upload=parser.get('URLs', 'dict_upload')
dict_remove=parser.get('URLs', 'dict_remove')
backend=parser.get('URLs', 'backend')
broker=parser.get('URLs', 'broker')
