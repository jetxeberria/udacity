import pytest

from udacity import lesson_3_final_exercise as l3
from tests.helpers import lesson_3_final_exercise as l3h


def test_decorator_factory():
    assert l3h.foo(2,"acX")


@pytest.mark.parametrize(
    "target_fn, fake_args, fake_kwargs",
    [
        (
            sum, 
            [[1, 2, 3]],
            {}
        ),
        (
            print, 
            ["one", "two", "three"],
            {"sep": ":", "end": "\n\n"}
        ),
        (
            l3h.foo, 
            [2, "seX"],
            {}
        )
    ]
)
def test_g_function_with_args_w_bind_args_t_binded(target_fn, fake_args, fake_kwargs):
    signature = l3.get_signature(target_fn)
    if not signature:
        return
    binded = l3.bind_args(signature, *fake_args, **fake_kwargs)
    assert all(
        [
            a in binded.values()
            for a in fake_args
            if fake_args and binded
        ]
    )
    assert all(
        [
            a in binded.values()
            for a in fake_kwargs
            if fake_kwargs and binded
        ]
    )

# @pytest.mark.parametrize(
#     "target_fn, fake_args, fake_kwargs",
#     [
#         (
#             sum, 
#             [[1, 2, 3]],
#             {}
#         ),
#         (
#             print, 
#             ["one", "two", "three"],
#             {"sep": ":", "end": "\n\n"}
#         )
#     ]
# )
# def test_given_invalid_arg_when_checked_then_fail(target_fn, fake_args, fake_kwargs):
#     assert target_fn(fake_args, fake_kwargs)


def test_given_invalid_arg_when_checked_then_fail():
    assert l3h.foo(2,"acX")
    with pytest.raises(l3.AnnotationError):
        l3h.foo("a","acX")
    with pytest.raises(l3.AnnotationError):
        l3h.foo(2,2)
