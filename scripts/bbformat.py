import os
import re


def format_bbcode(row, peers):
    target = '[/url]'

    results = row.split(target)
    output = ''
    counter = 0
    for i in results:
        counter += 1
        i += target
        output += i
        if counter == peers:
            output += '\n'
            counter = 0
    with open('output.txt', 'w') as out:
        out.write(output[:-6])


def remove_url(raw, peers):
    result = re.findall(r'(?<=])https?://.+?\.png', raw)
    if not result:
        result = re.findall(r'(?<=src=")https?://.+?\.png', raw)
    counter = 0
    output = ''
    for i in result:
        counter += 1
        i = "[img]{}[/img]\n".format(i.strip())

        if counter == peers:
            i += '\n'
            counter = 0
        output += i
    with open('output.txt', 'w') as out:
        out.write(output)


def read_file():
    with open('input.txt', 'r') as r:
        out = r.read()
        return out


if __name__ == "__main__":
    a = input('请输入需要处理的数据：') if 'input.txt' not in os.listdir() else read_file()
    b = int(input('请输入参与对比个数：'))
    option = input('请输入需要使用的模式：\n1.格式化换行略缩图bbcode\n2.删除图片模式中的无关内容并(或)格式化原图\n')
    if option == '1':
        format_bbcode(a, b)
    else:
        remove_url(a, b)
