from argparsing.functions.colors import Colors
import re


def get_employee_position(args):
    if args.position[0].lower() == 'manager':
        return 'manager'
    elif args.position[0].lower() == 'salesperson':
        return 'salesperson'
    else:
        return None


def employee_filename(fullname):
    file_name = fullname + '_records.txt'
    return file_name


def get_item_to_sell(item_name, available_items):
    print('You can sell the following {}s:'.format(item_name))
    for item in available_items:
        print(Colors.GREEN + item + Colors.RESET)
    item_to_sell = input('Enter ' + item_name + ' name: \n')
    return item_to_sell


def enter_price(item):
    while True:
        user_price = input('Enter ' + item + ' price: \n')
        try:
            beverage_price = float(user_price)
            if beverage_price < 0:
                print('You can enter only positive integers or floats.\nTry Again!')
                continue
            break
        except ValueError:
            print('"{}" is not a number. You can enter only positive integers or floats\nTry again!'.format(user_price))
    return str(beverage_price)


def beverage_to_file(file_name, beverage_record='Default beverage'):
    try:
        with open(file_name, 'a') as f:
            f.write(beverage_record + '\n')
    except IOError as e:
        ('File not found or path is incorrect... {}'.format(e))


def beverage_addition_to_file(file_name, beverage_record='Default beverage', addition_record='Default addition'):
    try:
        with open(file_name, 'a') as f:
            f.write(beverage_record + '\n')
            f.write(addition_record + '\n')
    except IOError as e:
        print('File not found or path is incorrect... {}'.format(e))


def show_sales_table(employees):
    sales_sum = sum([pair[2] for pair in employees])
    amount_sum = sum([pair[3] for pair in employees])

    seller_name = Colors.GREEN + 'Seller Name' + Colors.RESET
    num_of_sales = Colors.GREEN + 'Number Of Sales' + Colors.RESET
    total_val = Colors.GREEN + 'Total Value ($)' + Colors.RESET

    print('{:<39}\t|\t{:<5}\t|\t{}'.format(seller_name, num_of_sales, total_val))
    for _, name, sales, amount in employees:
        print('{:<30}\t|\t{:<15}\t|\t{}'.format(name, sales, amount))
    print('{:<30}\t|\t{:<15}\t|\t{}\t\n'.format('Total:', sales_sum, amount_sum))


def match_price(total_price_list, regexp, line):
    result = re.findall(regexp, line)
    price = float(result[0])
    total_price_list.append(price)
    return total_price_list
