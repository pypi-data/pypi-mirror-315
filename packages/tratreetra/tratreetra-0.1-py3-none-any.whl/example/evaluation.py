""" Script for evaluating the system's output against the gold treebank """
import utils_evalud

if __name__ == "__main__":

    print("Evaluating the test set...")
    orig_fp, fixed_fp = ("UD_Kyrgyz-TueCL/ky_tuecl-ud-test.conllu",
                         "data/ky_tuecl-ud-test-fixed.conllu")

    with open(orig_fp, "r", encoding="utf-8") as rf:
        with open(fixed_fp, "w", encoding="utf-8") as wf:
            wf.write(rf.read()
                     .replace("ѳ", "ө")
                     .replace("Ѳ", "ө"))

    gold = utils_evalud.load_conllu_file("data/ky_tuecl-ud-test-fixed.conllu")

    for conv_file in ["data/out.conllu"]:
        print(conv_file)
        system = utils_evalud.load_conllu_file(conv_file)
        results_dict = utils_evalud.evaluate(gold, system)
        eval_table_rat = utils_evalud.build_evaluation_table(results_dict,
                                                             verbose=True,
                                                             counts=False,
                                                             enhanced=False)

        print(eval_table_rat)
