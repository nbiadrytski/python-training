from argparsing.functions.colors import Colors
import re
import logging

logger = logging.getLogger('main.argparsing.functions.functions')


def get_employee_position(args):
    """
    Getting lowercase employee position from passed command line argument.

    Parameters:
        args (argparse.Namespace): Arguments passed via command line.

    Returns:
        str: 'manager' if Manager position passed, 'salesperson' if Salesperson position passed, else None.
    """
    if args.position[0].lower() == 'manager':
        logger.debug('get_employee_position(): employee is a manager')
        return 'manager'
    elif args.position[0].lower() == 'salesperson':
        logger.debug('get_employee_position(): employee is a salesperson')
        return 'salesperson'
    else:
        logger.debug('get_employee_position(): employee is neither a salesperson nor a manager')
        return None


def employee_filename(fullname):
    """
    Creates file name based on Employee full name.

    Parameters:
        fullname (str): Employee full name.

    Returns:
        str: file name
    """
    file_name = fullname + '_records.txt'
    logger.debug('employee_filename(): {} file created'.format(file_name))
    return file_name


def get_item_to_sell(item_name, available_items):
    """
    Returns beverage or ingredient which can be sold (validated by provided command line arguments) based on user input.

    Parameters:
        item_name (str): Beverage or addition name.
        available_items (list): list of available beverages or ingredients.

    Returns:
        str: beverage or addition which can be sold.
    """
    print('You can sell the following {}s:'.format(item_name))
    for item in available_items:
        print(Colors.GREEN + item + Colors.RESET)
    item_to_sell = input('Enter ' + item_name + ' name: \n')
    logger.debug('get_item_to_sell(): salesperson wants to sell {}'.format(item_to_sell))
    return item_to_sell


def enter_price(item):
    """
    Returns beverage or ingredient price from user input. User input validation:
    Price should be greater than zero.
    Price should be only positive integer or float.
    The following prices can be accepted, e.g: 4, 4.0, 4.3, 4.39, 4.45687

    Parameters:
        item (str): 'beverage' or 'ingredient' string.

    Returns:
        str: beverage or addition price.

    Raises:
        ValueError: If price is not a number.
    """
    while True:
        user_price = input('Enter ' + item + ' price: \n')
        try:
            item_price = float(user_price)
            if item_price < 0:
                print('You can enter only positive integers or floats.\nTry Again!')
                continue
            break
        except ValueError:
            print('"{}" is not a number. You can enter only positive integers or floats\nTry again!'.format(user_price))
    logger.debug('enter_price(): salesperson wants to set price "{}"'.format(str(item_price)))
    return str(item_price)


def beverage_to_file(file_name, beverage_record='Default beverage'):
    """
    Writes beverage record to file in 'append' mode

    Parameters:
        file_name (str): pass Salesperson.employee_filename() function.
        beverage_record (str): pass Salesperson.add_beverage() method. 'Default beverage' is default value.

    Raises:
        IOError: If file not found or path is incorrect.
    """
    try:
        with open(file_name, 'a') as f:
            f.write(beverage_record + '\n')
            logger.debug('beverage_to_file(): wrote beverage "{}" to {} file'.format(beverage_record, file_name))
    except IOError as e:
        logger.error('File {} not found or path is incorrect... {}'.format(file_name, e))


def beverage_addition_to_file(file_name, beverage_record='Default beverage', addition_record='Default addition'):
    """
    Writes beverage and ingredient record to file in 'append' mode.

    Parameters:
        file_name (str): pass Salesperson.employee_filename() function.
        beverage_record (str): pass Salesperson.add_beverage() method. 'Default beverage' is default value.
        addition_record (str): pass Salesperson.beverage_addition_to_file() method. 'Default addition' is default value.

    Raises:
        IOError: If file not found or path is incorrect.
    """
    try:
        with open(file_name, 'a') as f:
            f.write(beverage_record + '\n')
            f.write(addition_record + '\n')
            logger.debug('beverage_addition_to_file(): wrote beverage "{}" and addition {} to {} file'.
                         format(beverage_record, addition_record, file_name))
    except IOError as e:
        logger.error('File {} not found or path is incorrect... {}'.format(file_name, e))


def show_sales_table(employees):
    """
    Printing formatted table with salespeople records to Manager.

    Parameters:
        employees (list): list of salespeople returned by view_db_records() function.

    Raises:
        TypeError: If cannot iterate over empty/non-existing salespeople list.
    """
    try:
        sales_sum = sum([pair[2] for pair in employees])
        amount_sum = sum([pair[3] for pair in employees])
        logger.debug('show_sales_table(): number of sales sum: {}, total amount sum: {}'.
                     format(str(sales_sum), str(amount_sum)))
        seller_name = Colors.GREEN + 'Seller Name' + Colors.RESET
        num_of_sales = Colors.GREEN + 'Number Of Sales' + Colors.RESET
        total_val = Colors.GREEN + 'Total Value ($)' + Colors.RESET
        # printing sales records in formatted table
        print('{:<39}\t|\t{:<5}\t|\t{}'.format(seller_name, num_of_sales, total_val))
        for _, name, sales, amount in employees:
            print('{:<30}\t|\t{:<15}\t|\t{}'.format(name, sales, amount))
        print('{:<30}\t|\t{:<15}\t|\t{}\t\n'.format('Total:', sales_sum, amount_sum))
    except TypeError as e:
        logger.info('Cannot iterate over empty/non-existing employees list... {}'.format(e))


def match_price(total_price_list, regexp, line):
    """
    Appends prices to list by provided regexp. Can be used in:
    Salesperson.total_sales_amount() method to calculate total price.

    Parameters:
        total_price_list (list): empty list.
        regexp (str): regular expression.
        line (str): line to look through.

    Returns:
        list: List with prices.
    """
    result = re.findall(regexp, line)
    price = float(result[0])
    total_price_list.append(price)
    logger.debug('match_price(): total price list: {}'.format(str(total_price_list)))
    return total_price_list
