import argparse

import crawler
import record

"""
Useful Documents and Tutorial:

"""

"""
Usage:
1. Get recommended unsolved practice problems based on frequency
2. Get recommended reviewed practice problems based on records
3. Add finished problems to records
4. Add reviewed problems to records
"""
def get_new_problem(args):
    problems = crawler.crawlerLeetcode.get_problems_info()
    problems['stat_status_pairs'].sort(key=lambda problem: -problem['frequency'])

    records = {int(record[1]): record for record in record.leetcodeRecord.read_records_file()}

    recommendation = []
    difficulty = {1: "Easy", 2: "Medium", 3: "Hard"}

    for problem in problems['stat_status_pairs']:
        if problem['stat']['frontend_question_id'] not in records:
            recommendation.append((problem['stat']['frontend_question_id'],
                                   problem['stat']['question__title'],
                                   difficulty[problem['difficulty']['level']]))

            if len(recommendation) == args.get_new_problem:
                break

    for recommend in recommendation:
        print recommend


def get_review_problem(args):
    records = record.leetcodeRecord.read_records_file()
    records.sort(key=lambda record: record[3].count('n') / float(len(record[3])))

    for idx in range(min(args.get_review, len(records))):
        print records[idx][:-1]


def add_finish_to_records(args):
    record.leetcodeRecord.write_record_to_file(args.finish)


def add_review_to_records(args):
    record.leetcodeRecord.update_review_by_id(args.review)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Management Tool for Leetcode Practice")

    parser.add_argument("--get_new_problem", help="get recommended problems", type=int)
    parser.add_argument("--get_review", help="get reviewed problems", type=int)
    parser.add_argument("--finish", help="add finished problems to record, format: Day | Question_Id | Question_Title | Need_Review | Comments", nargs=5)
    parser.add_argument("--review", help="add reviewed problems to record, format: Question_Id | Need_Review | Comments", nargs=3)

    args = parser.parse_args()
    if args.get_new_problem:
        get_new_problem(args)
    elif args.get_review:
        get_review_problem(args)
    elif args.finish:
        add_finish_to_records(args)
    elif args.review:
        add_review_to_records(args)
    else:
        parser.print_help()