# # -*- coding: utf-8 -*-

# import multiprocessing
# import json
# import traceback
# import warnings
# from copy import deepcopy
# from itertools import product
# from src.database.database import Database

# def permutations(componentdict):
#     for v in product(*componentdict.values()):
#         yield dict(zip(componentdict, v))

# def execute(d_dict: dict, code_string: str) -> dict:    #type:ignore
#     try:
#         exec(code_string, locals(), d_dict)
#     except Exception:
#         warnings.warn("exception while exec_()")
#         print(f'state:\n{json.dumps(d_dict, indent=2)}')
#         print(f'condtion:{code_string}')
#         traceback.print_exc()
#     else:
#         return d_dict

# def evaluate(state, rules, triggerDict):

#     for k, v in state.items():
#         locals()[k] = v
#     init_dict = deepcopy(state)
#     final_dict = deepcopy(state)

#     for rule in rules:
#         final_dict = execute(final_dict, rule)

#     if init_dict == final_dict:
#         validTestCases = list()
#         for trigger in triggerDict:                         # each key
#             for triggerState in triggerDict.get(trigger):   # each state
#                 _flag, \
#                 initialState, \
#                 expectedState = evaluate_tc(state=state, \
#                                             rules=rules, \
#                                             trigger={trigger: triggerState})    #type:ignore
#                 if _flag:
#                     validTestCases.append({
#                     "testTrigger": {trigger: triggerState},
#                     "initialState": initialState,
#                     "expectedState": expectedState
#                     })

#         if(len(validTestCases)==0):
#             warnings.warn("valid state but return 0 test cases!")
#         return (True, validTestCases)
#     elif init_dict != final_dict:
#         return (False, False)

# def evaluate_tc(state, rules, trigger):

#     init_dict = deepcopy(state)
#     expected_dict = deepcopy(state)

#     for k, v in trigger.items():
#         expected_dict[k] = v

#     for k, v in expected_dict.items():
#         locals()[k] = v

#     for rule in rules:
#         expected_dict = execute(expected_dict, rule)

#     if expected_dict == init_dict:
#         return (False, {}, {})
#     elif expected_dict != init_dict:
#         return (True, init_dict, expected_dict)


# class Executor:
#     def __init__(self, database_loc, process_num, batch_size):

#         self.pool = multiprocessing.Pool(process_num)
#         self.Database = database_loc
#         self.BatchSize = batch_size
#         self.countInvalid = 0
#         self.countValid = 0
#         self.countTestCases = 0
#         self.countTotal = 0
#         self.listTestCases = list()

#     def printLegend(self):
#         print(f"\n\n{60*'-'}\nTotal States : T\nValid States : VS\nInvalid States : InS\nTest Cases : TC\n")


#     def _pushToDatabase(self):

#         try:
#             t_dbObject = Database(self.Database)
#             t_dbObject.InsertTestCases(self.listTestCases)
#         except Exception:
#             warnings.warn("exception pushing to database")
#         else:
#             # print("pushing")
#             pass
#         finally:
#             self.listTestCases.clear()


#     def callback_(self, result):

#         flag, testcases = result[0], result[1]

#         if not flag:
#             self.countInvalid += 1
#         else:
#             self.countValid += 1
#             self.countTestCases += len(testcases)

#             for tc in testcases:
#                 self.listTestCases.append(tc)

#         print(f"\rT:{self.countTotal} VS:{self.countValid} InS:{self.countInvalid} TC:{self.countTestCases}", end=" ")
#         if len(self.listTestCases) >= self.BatchSize:
#             self._pushToDatabase()


#     def schedule(self, function, args):
#         self.countTotal += 1
#         self.pool.apply_async(function, args=args, callback=self.callback_)


#     def terminate(self):
#         self.pool.close()
#         self.pool.join()
#         print(f"\rT:{self.countTotal} VS:{self.countValid} InS:{self.countInvalid} TC:{self.countTestCases}")
#         print(f"{60*'-'}\n")
#         self._pushToDatabase()



