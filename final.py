from speech import record
from module import main

# def final(count):
#     stage1_result = record(count)
#     print(stage1_result)
#     # if(stage1_result[0]):
#     #     stage2_result=main(stage1_result[1])
#     #     if not stage2_result:
#     #         final(stage1_result[1]+1)
    
# final(0)

stage1_result = record(0)
if(stage1_result):
    main(0)
