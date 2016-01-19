from filecmp import cmp
from tokenize import TokenInfo
from behave import *
from nose.tools.trivial import ok_

use_step_matcher("re")

import os
script_dir = os.path.dirname(__file__)

from of.broker.lib.translation.python.translator import ProcessTokens


@given("a source file is tokenized")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    _definitions = ProcessTokens.load_definitions(_definition_files=[os.path.join(script_dir, "../fake_bpm_lib.json")])
    context.tokens = ProcessTokens(_definitions = _definitions)
    context.verbs = context.tokens.parse_file(os.path.join(script_dir, "../source.py"))


@then("the output must match spot check verbs")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    ok_(context.verbs[6].children[1].children[0].identifier == 'print' and context.verbs[6].children[1].children[0].parameters == {'expression': '"This should always happen three times."'})



@given("an array of verb is converted to json")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    context.json = ProcessTokens.verbs_to_json(context.verbs)


@then("the output must match spot check json")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    ok_(context.json[6]["children"][1]["children"][0]["identifier"] == 'print' and context.json[6]["children"][1]["children"][0]["parameters"] == {'expression': '"This should always happen three times."'})


@step("it is converted back to verbs")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    try:
        context.verbs = ProcessTokens.json_to_verbs(context.json)
    except Exception as e:
        print(str(e))

@step("is untokenized into another file")
def step_impl(context):
    """
    :type context behave.runner.Context
    """

    _definitions = context.tokens.encode_verbs(context.verbs, context.tokens.raw, os.path.join(script_dir, "../source_out.py"))


@then("the files must match")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    ok_(cmp(os.path.join(script_dir, "../source.py"), os.path.join(script_dir, "../source_out.py"), "Files do not match!"))


@step("all verbs raw property is reset")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    def reset_verbs_recursively(_verb):
        _verb.raw = None
        for _curr_child in _verb.children:
            reset_verbs_recursively(_curr_child)

    for _curr_child in context.verbs:
        reset_verbs_recursively(_curr_child)
