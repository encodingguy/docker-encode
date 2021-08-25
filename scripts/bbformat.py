import re


def format_bbcode(row):
    target = '[/url]'

    peers = int(input('请输入参与对比个数：'))

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


def remove_url(raw):
    result = re.findall(r'(?<=])https?://.+?\.png', raw)
    if not result:
        result = re.findall(r'(?<=src=")https?://.+?\.png', raw)
    result = ["[img]{}[/img]\n".format(i) for i in result]
    with open('output.txt', 'w') as out:
        out.writelines(result)


if __name__ == "__main__":
    a = input('请输入需要处理的数据：')
    option = input('请输入需要使用的模式：\n1. 格式化换行bbcode\n2.删除图片模式中的无关内容\n')
    if option == '1':
        format_bbcode(a)
    else:
        remove_url(a)
