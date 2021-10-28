def doubler(num):
    """
    Given a

    """
    result = number * 2
    return result


if __name__ == '_main_':

    try:
        input = float(sys.argv[1])

    except:
        print('Error')
        sys.exit(1)

    answer = doubler(input)
    print(answer)