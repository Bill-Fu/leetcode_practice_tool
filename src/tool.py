# coding=utf-8
import argparse
import crawlerLib
import datetime
import recordLib

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
    problems = crawlerLib.crawlerLeetcode.get_problems_info()['stat_status_pairs']
    problems.sort(key=lambda problem: -problem['frequency'])

    recordTable = {record[recordLib.RecordField.QUESTION_ID.value - 1]: record for record in recordLib.leetcodeRecord.read_record()}

    recommendation = []

    for problem in problems:
        if str(problem['stat']['frontend_question_id']) not in recordTable and crawlerLib.Difficulty(problem['difficulty']['level']) != crawlerLib.Difficulty.HARD:
            recommendation.append((problem['stat']['frontend_question_id'],
                                   problem['stat']['question__title'],
                                   crawlerLib.Difficulty(problem['difficulty']['level']).name))

            if len(recommendation) == args.get_new_problem:
                break

    print("%5s %76s %13s" % (u"题号", u"题目", u"难度"))
    for recommend in recommendation:
        print("%5s %80s %15s" % (recommend[0], recommend[1], recommend[2]))


def get_review_problem(args):
    records = recordLib.leetcodeRecord.read_record()
    records.sort(key=lambda record: record[recordLib.RecordField.NEED_REVIEW.value - 1].count('n') / float(len(record[3])))

    print("%1s %3s %78s %6s %s" % (u"日期", u"题号", u"题目", u"复习记录", u"备注") )
    for record in records[:min(args.get_review_problem, len(records))]:
        print("%3s %5s %80s %10s %s" % (record[recordLib.RecordField.DAY.value - 1],
                                        record[recordLib.RecordField.QUESTION_ID.value - 1],
                                        record[recordLib.RecordField.QUESTION_TITLE.value - 1],
                                        record[recordLib.RecordField.NEED_REVIEW.value - 1],
                                        record[recordLib.RecordField.COMMENTS.value - 1]))


def add_new_problem(args):
    records = recordLib.leetcodeRecord.read_record()
    recordTable = {record[recordLib.RecordField.QUESTION_ID.value - 1]: record for record in recordLib.leetcodeRecord.read_record()}

    problems = crawlerLib.crawlerLeetcode.get_problems_info()['stat_status_pairs']
    problemTable = {str(problem['stat']['frontend_question_id']): problem['stat']['question__title'] for problem in problems}

    if args.add_new_problem[0] in recordTable:
        print(u"题目已经完成过，可能您想要添加该题的复习记录?")
        return
    elif args.add_new_problem[0] not in problemTable:
        print(u"题号不存在，请检查输入")
        return

    record = [
        str(int(records[-1][recordLib.RecordField.DAY.value - 1]) if datetime.date.today() == records[-1][recordLib.RecordField.DATE.value - 1] else int(records[-1][recordLib.RecordField.DAY.value - 1]) + 1),
        args.add_new_problem[0],
        problemTable[args.add_new_problem[0]],
        args.add_new_problem[1],
        args.add_new_problem[2],
        datetime.date.today()
    ]

    recordLib.leetcodeRecord.add_record(record)


def add_review_problem(args):
    matchedRecords = recordLib.leetcodeRecord.read_record(field=recordLib.RecordField.QUESTION_ID.value, value=args.add_review_problem[0])

    if not matchedRecords:
        print(u"题目记录不存在，请检查输入")
        return
    elif len(matchedRecords) > 1:
        # 目前应该不会出现重复记录的问题
        print(u"重复题目记录，请检查记录")
        return

    oldRecord = matchedRecords[0]
    updatedRecord = [
        oldRecord[recordLib.RecordField.DAY.value - 1],
        oldRecord[recordLib.RecordField.QUESTION_ID.value - 1],
        oldRecord[recordLib.RecordField.QUESTION_TITLE.value - 1],
        oldRecord[recordLib.RecordField.NEED_REVIEW.value - 1] + args.add_review_problem[1],
        oldRecord[recordLib.RecordField.COMMENTS.value - 1] + "\n" + args.add_review_problem[2].decode('utf-8'),
        oldRecord[recordLib.RecordField.DATE.value - 1]
    ]

    recordLib.leetcodeRecord.update_record(field=recordLib.RecordField.QUESTION_ID.value, value=args.add_review_problem[0], record=updatedRecord)


def query(args):
    matchedRecords = recordLib.leetcodeRecord.read_record(field=recordLib.RecordField.QUESTION_ID.value, value=args.query)

    if not matchedRecords:
        print(u"该题目练习记录不存在")
        return
    elif len(matchedRecords) > 1:
        # 目前应该不会出现重复记录的问题
        print(u"重复题目记录，请检查记录")
        return

    record = matchedRecords[0]

    print("%1s %3s %78s %6s %s" % (u"日期", u"题号", u"题目", u"复习记录", u"备注"))
    print("%3s %5s %80s %10s %s" % (record[recordLib.RecordField.DAY.value - 1],
                                    record[recordLib.RecordField.QUESTION_ID.value - 1],
                                    record[recordLib.RecordField.QUESTION_TITLE.value - 1],
                                    record[recordLib.RecordField.NEED_REVIEW.value - 1],
                                    record[recordLib.RecordField.COMMENTS.value - 1]))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=u"Leetcode刷题管理工具")

    parser.add_argument("--get_new_problem", help=u"查询今日新练习题目, 格式: 获取题目数量", type=int)
    parser.add_argument("--get_review_problem", help=u"查询今日复习题目, 格式: 获取题目数量", type=int)
    parser.add_argument("--add_new_problem", help=u"添加新练习题目, 格式: 题号 | 复习记录 | 备注", nargs=3)
    parser.add_argument("--add_review_problem", help=u"添加复习题目, 格式: 题号 | 复习记录 | 备注", nargs=3)
    parser.add_argument("--query", help=u"查询题目练习情况, 格式: 题号", type=str)

    args = parser.parse_args()
    if args.get_new_problem:
        get_new_problem(args)
    elif args.get_review_problem:
        get_review_problem(args)
    elif args.add_new_problem:
        add_new_problem(args)
    elif args.add_review_problem:
        add_review_problem(args)
    elif args.query:
        query(args)
    else:
        parser.print_help()