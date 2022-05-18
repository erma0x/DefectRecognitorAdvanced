import argparse

'''
impara a passare gli argomenti dello script con argparse
'''
parser = argparse.ArgumentParser()
parser.add_argument('x', type=float)
parser.add_argument('y', type=float)
args = parser.parse_args()

print(args.x + args.y)
