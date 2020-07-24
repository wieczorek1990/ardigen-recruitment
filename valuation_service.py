#!/usr/bin/env python3

import csv


BASE_CURRENCY = 'PLN'


def load_csv(filename, viewer=None, fetcher=None):
    with open(filename) as csv_file:
        reader = csv.reader(csv_file)
        if viewer is not None:
            viewer(reader)
        if fetcher is not None:
            return fetcher(reader)


def print_csv(reader):
    for row in reader:
        print(', '.join(row))
    print('')


def currency_all_same(records, currency):
    list_ = map(lambda x: x[2], records)
    result = True
    for element in list_:
        result = result and element == currency
    return result


def compute_result(data, currencies, matchings):
    top = {}
    for matching_id, records in data.items():
        records.sort(key=lambda x: -x[1] * currencies[x[2]] * x[3])
        top[matching_id] = records

    result = {}
    for matching_id, top_priced_count in matchings.items():
        result[matching_id] = {
                'matching_id': matching_id,
                'ignored_products_count': len(top[matching_id][top_priced_count:])
        }
        top[matching_id] = top[matching_id][:top_priced_count]

    for matching_id, records in top.items():
        try:
            first_currency = records[0][2]
            if currency_all_same(records, first_currency):
                currency = first_currency
            else:
                currency = BASE_CURRENCY
            total_price = 0
            total_quantity = 0
            for record in records:
                total_quantity += record[3]
                if currency == BASE_CURRENCY:
                    total_price += currencies[currency] * record[3] * record[1]
                else:
                    total_price += record[3] * record[1]
            result[matching_id]['currency'] = currency
            result[matching_id]['total_price'] = total_price
            result[matching_id]['avg_price'] = round(total_price / total_quantity, 2)
        except KeyError:
            print('Invalid data, empty data set')
            exit(1)
    return result


def write_result(result):
    with open('top_products.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['matching_id', 'total_price', 'avg_price', 'currency', 'ignored_products_count'])
        for row in result.values():
            writer.writerow([row['matching_id'],
                             row['total_price'],
                             row['avg_price'],
                             row['currency'],
                             row['ignored_products_count']])


def data_fetcher(reader):
    result = {}
    header = True
    for identifier, price, currency, quantity, matching_id in reader:
        if header:
            header = False
            continue
        record = (int(identifier), int(price), currency, int(quantity))
        matching_id = int(matching_id)
        if matching_id not in result:
            result[matching_id] = [record]
        else:
            result[matching_id].append(record)
    return result


def currencies_fetcher(reader):
    result = {}
    header = True
    for name, ratio in reader:
        if header:
            header = False
            continue
        result[name] = float(ratio)
    return result


def matchings_fetcher(reader):
    result = {}
    header = True
    for matching_id, top_priced_count in reader:
        if header:
            header = False
            continue
        result[int(matching_id)] = int(top_priced_count)
    return result


def main():
    data = load_csv('data.csv', fetcher=data_fetcher)
    currencies = load_csv('currencies.csv', fetcher=currencies_fetcher)
    matchings = load_csv('matchings.csv', fetcher=matchings_fetcher)
    result = compute_result(data, currencies, matchings)
    write_result(result)


if __name__ == '__main__':
    main()
