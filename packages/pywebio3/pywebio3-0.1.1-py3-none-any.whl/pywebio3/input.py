import copy
import logging
import os.path
from collections.abc import Mapping
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from .io_ctrl import input_control, output_register_callback, send_msg, single_input, single_input_kwargs
from .platform import page as platform_setting
from .session import get_current_session, get_current_task_id
from .utils import Setter, check_dom_name_value, parse_file_size

logger = logging.getLogger(__name__)

TEXT = 'text'
NUMBER = "number"
FLOAT = "float"
PASSWORD = "password"
URL = "url"
DATE = "date"
TIME = "time"
COLOR = "color"
DATETIME_LOCAL = "datetime-local"
DATETIME = DATETIME_LOCAL

CHECKBOX = 'checkbox'
RADIO = 'radio'
SELECT = 'select'
TEXTAREA = 'textarea'

__all__ = ['TEXT', 'NUMBER', 'FLOAT', 'PASSWORD', 'URL', 'DATE',
           'TIME', 'COLOR', 'DATETIME_LOCAL', 'DATETIME', 'input', 'textarea',
           'select', 'checkbox', 'radio', 'actions', 'file_upload',
           'slider', 'input_group', 'input_update']


def _parse_args(kwargs, excludes=()):
    """parse the raw parameters that pass to input functions

     - excludes: the parameters that don't appear in returned spec
     - remove the parameters whose value is None

    :return:（spec，valid_func）
    """
    kwargs = {k: v for k, v in kwargs.items() if v is not None and k not in excludes}
    check_dom_name_value(kwargs.get('name', ''), '`name`')

    kwargs.update(kwargs.get('other_html_attrs', {}))
    kwargs.pop('other_html_attrs', None)

    if kwargs.get('validate'):
        kwargs['onblur'] = True
    valid_func = kwargs.pop('validate', lambda _: None)

    if kwargs.get('onchange'):
        onchange_func = kwargs['onchange']
        kwargs['onchange'] = True
    else:
        onchange_func = lambda _: None

    return kwargs, valid_func, onchange_func


def input(
        label: str = '',
        type: str = TEXT, *,
        validate: Callable[[Any], Optional[str]] = None,
        name: str = None,
        value: Union[str, int] = None,
        action: Tuple[str, Callable[[Callable], None]] = None,
        onchange: Callable[[Any], None] = None,
        placeholder: str = None, required: bool = None,
        readonly: bool = None,
        datalist: List[str] = None,
        help_text: str = None,
        **other_html_attrs,
):
    """
    录入文本
    :param label: 标签
    :param type: 输入类型：`TEXT` , `NUMBER` , `FLOAT` , `PASSWORD` , `URL` , `DATE` , `TIME`, `DATETIME`, `COLOR`。
        时间类型 `DATE` , `TIME`, `DATETIME` 的值是格式化的字符串 `YYYY-MM-DD` , `HH:MM:SS` , `YYYY-MM-DDTHH:MM`
    :param validate：校验方法，成功返回None，失败返回错误信息，示例
            def check_age(age):
                if age>30:
                    return 'Too old'
                elif age<10:
                    return 'Too young'
            input('Input your age', type=NUMBER, validate=check_age)
    :param name: 指定输入名称的字符串。与input_group一起使用，用于识别输入组结果中的不同输入项。如果单独调用输入函数，该参数可以**不设置！
    :param value: 输入的初始值
    :param action: tuple(label:str, callback:callable)
    :param action: 在输入字段的右侧放置一个按钮，用户可以单击该按钮来设置输入的值。label ’是按钮的标签，
            callback是点击时设置输入值的回调函数。调用回调时只有一个参数，即set_value。
            set_value是一个可调用的对象，它被一个或两个参数调用。您可以使用set_value来设置输入的值。
            set_value可以通过一个参数调用：set_value(value:str)。
            value参数是要为输入设置的值。
            set_value可以通过两个参数调用：set_value(value:any, label:str)。每个参数描述如下：
         * ``value`` : The real value of the input, can be any object. it will not be passed to the user browser.
         * ``label`` : The text displayed to the user

        When calling ``set_value`` with two arguments, the input item in web page will become read-only.

        The usage scenario of ``set_value(value:any, label:str)`` is: You need to dynamically generate the value of the
        input in the callback, and hope that the result displayed to the user is different from the actual submitted data
        (for example, result displayed to the user can be some user-friendly texts, and the value of the input can be
        objects that are easier to process)

        Usage example:

        .. exportable-codeblock::
            :name: input-action
            :summary: `input()` action usage

            import time
            def set_now_ts(set_value):
                set_value(int(time.time()))

            ts = input('Timestamp', type=NUMBER, action=('Now', set_now_ts))
            put_text('Timestamp:', ts)  # ..demo-only
            ## ----
            from datetime import date,timedelta
            def select_date(set_value):
                with popup('Select Date'):
                    put_buttons(['Today'], onclick=[lambda: set_value(date.today(), 'Today')])
                    put_buttons(['Yesterday'], onclick=[lambda: set_value(date.today() - timedelta(days=1), 'Yesterday')])

            d = input('Date', action=('Select', select_date), readonly=True)
            put_text(type(d), d)

        Note: When using :ref:`Coroutine-based session <coroutine_based_session>` implementation, the ``callback``
        function can be a coroutine function.

    :param callable onchange: 一个回调函数，当用户改变这个输入字段的值时将被调用。调用onchange回调时使用一个参数，即输入字段的当前值。onchange的典型使用场景是通过input_update()来更新其他输入项。
    :param placeholder: 提示用户可以在输入中输入什么内容。当没有设置值时，它将出现在输入字段中。
    :param required: 是否需要一个值来提交输入，默认值是False
    :param readonly: 该值是否为只读（不可编辑）
    :param datalist: 向用户建议此输入的预定义值列表。只能在“type=TEXT”时使用。
    :param help_text: 用于输入的帮助文本。文本将以小字体显示在输入字段下方
    :param other_html_attrs: 添加到input元素的附加html属性。

    :return: 用户输入的值。
    """

    item_spec, valid_func, onchange_func = _parse_args(locals(), excludes=('action',))

    # check input type
    allowed_type = {TEXT, NUMBER, FLOAT, PASSWORD, URL, DATE, TIME, COLOR, DATETIME_LOCAL}
    assert type in allowed_type, 'Input type not allowed.'

    value_setter = None
    if action:
        label, callback = action
        task_id = get_current_task_id()

        value_setter = Setter()

        def _set_value(value, label=value_setter):
            spec = {
                'target_name': item_spec.get('name', 'data'),
                'attributes': {'value': value}
            }
            if label is not value_setter:
                value_setter.label = label
                spec['attributes']['value'] = label
                spec['attributes']['readonly'] = True
            value_setter.value = value
            msg = dict(command='update_input', task_id=task_id, spec=spec)
            get_current_session().send_task_command(msg)

        callback_id = output_register_callback(lambda _: callback(_set_value))
        item_spec['action'] = dict(label=label, callback_id=callback_id)

    def preprocess_func(d):  # Convert the original data submitted by the user
        if value_setter is not None and value_setter.label == d:
            return value_setter.value

        return d

    return single_input(item_spec, valid_func, preprocess_func, onchange_func)


def textarea(
        label: str = '',
        *,
        rows: int = 6,
        code: Union[bool, Dict] = None,
        maxlength: int = None,
        minlength: int = None,
        validate: Callable[[Any], Optional[str]] = None,
        name: str = None,
        value: str = None,
        onchange: Callable[[Any], None] = None,
        placeholder: str = None,
        required: bool = None,
        readonly: bool = None,
        help_text: str = None,
        **other_html_attrs,
):
    """
    文本输入区（多行文本输入）
    :param rows: 输入区域的可见文本行数。滚动条将在内容超过。
    :param int maxlength: 用户可以输入的最大字符数（UTF-16码单位）。如果未指定此值，则用户可以输入无限数量的字符。
    :param int minlength: 用户需要输入的最小字符数（UTF-16代码单元）。
    :param dict/bool code: 通过提供Codemirror <https://codemirror.net/> ’ _选项来启用代码样式编辑器
    :param label, validate, name, value, onchange, placeholder, required, readonly, help_text, other_html_attrs:  这些参数和 input() 的参数一样
    :return: 用户输入的字符串值。
    """
    item_spec, valid_func, onchange_func = _parse_args(locals())
    item_spec['type'] = TEXTAREA

    return single_input(item_spec, valid_func, lambda d: d, onchange_func)


def _parse_select_options(options):
    # Convert the `options` parameter in the `select`, `checkbox`, and `radio` functions to a unified format
    # Available forms of option:
    # {value:, label:, [selected:,] [disabled:]}
    # (value, label, [selected,] [disabled])
    # value (label same as value)
    opts_res = []
    for opt in options:
        opt = copy.deepcopy(opt)
        if isinstance(opt, Mapping):
            assert 'value' in opt and 'label' in opt, 'options item must have value and label key'
        elif isinstance(opt, (list, tuple)):
            assert len(opt) > 1 and len(opt) <= 4, 'options item format error'
            opt = dict(zip(('label', 'value', 'selected', 'disabled'), opt))
        else:
            opt = dict(value=opt, label=opt)
        opts_res.append(opt)

    return opts_res


def _set_options_selected(options, value):
    """set `selected` attribute for `options`"""
    if not isinstance(value, (list, tuple)):
        value = [value]
    for opt in options:
        if opt['value'] in value:
            opt['selected'] = True
    return options


def select(label: str = '', options: List[Union[Dict[str, Any], Tuple, List, str]] = None, *, multiple: bool = None,
           validate: Callable[[Any], Optional[str]] = None, name: str = None, value: Union[List, str] = None,
           onchange: Callable[[Any], None] = None, native: bool = True, required: bool = None, help_text: str = None,
           **other_html_attrs):
    r"""Drop-down selection

    By default, only one option can be selected at a time, you can set ``multiple`` parameter to enable multiple selection.

    :param list options: list of options. The available formats of the list items are:

        * dict::

            {
                "label":(str) option label,
                "value":(object) option value,
                "selected":(bool, optional) whether the option is initially selected,
                "disabled":(bool, optional) whether the option is initially disabled
            }

        * tuple or list: ``(label, value, [selected,] [disabled])``
        * single value: label and value of option use the same value

        Attention：

        1. The ``value`` of option can be any JSON serializable object
        2. If the ``multiple`` is not ``True``, the list of options can only have one ``selected`` item at most.

    :param bool multiple: whether multiple options can be selected
    :param value: The value of the initial selected item. When ``multiple=True``, ``value`` must be a list.
       You can also set the initial selected option by setting the ``selected`` field in the ``options`` list item.
    :type value: list or str
    :param bool required: Whether to select at least one item, only available when ``multiple=True``
    :param bool native: Using browser's native select component rather than
        `bootstrap-select <https://github.com/snapappointments/bootstrap-select>`_. This is the default behavior.
    :param - label, validate, name, onchange, help_text, other_html_attrs: Those arguments have the same meaning as for `input()`
    :return: If ``multiple=True``, return a list of the values in the ``options`` selected by the user;
        otherwise, return the single value selected by the user.
    """
    assert options is not None, 'Required `options` parameter in select()'

    item_spec, valid_func, onchange_func = _parse_args(locals(), excludes=['value'])
    item_spec['options'] = _parse_select_options(options)
    if value is not None:
        item_spec['options'] = _set_options_selected(item_spec['options'], value)
    item_spec['type'] = SELECT

    return single_input(item_spec, valid_func=valid_func, preprocess_func=lambda d: d, onchange_func=onchange_func)


def checkbox(label: str = '', options: List[Union[Dict[str, Any], Tuple, List, str]] = None, *, inline: bool = None,
             validate: Callable[[Any], Optional[str]] = None,
             name: str = None, value: List = None, onchange: Callable[[Any], None] = None, help_text: str = None,
             **other_html_attrs):
    r"""A group of check box that allowing single values to be selected/deselected.

    :param list options: List of options. The format is the same as the ``options`` parameter of the `select()` function
    :param bool inline: Whether to display the options on one line. Default is ``False``
    :param list value: The value list of the initial selected items.
       You can also set the initial selected option by setting the ``selected`` field in the ``options`` list item.
    :param - label, validate, name, onchange, help_text, other_html_attrs: Those arguments have the same meaning as for `input()`
    :return: A list of the values in the ``options`` selected by the user
    """
    assert options is not None, 'Required `options` parameter in checkbox()'

    item_spec, valid_func, onchange_func = _parse_args(locals(), excludes=['value'])
    item_spec['options'] = _parse_select_options(options)
    if value is not None:
        item_spec['options'] = _set_options_selected(item_spec['options'], value)
    item_spec['type'] = CHECKBOX

    return single_input(item_spec, valid_func, lambda d: d, onchange_func)


def radio(label: str = '', options: List[Union[Dict[str, Any], Tuple, List, str]] = None, *, inline: bool = None,
          validate: Callable[[Any], Optional[str]] = None,
          name: str = None, value: str = None, onchange: Callable[[Any], None] = None, required: bool = None,
          help_text: str = None, **other_html_attrs):
    r"""A group of radio button. Only a single button can be selected.

    :param list options: List of options. The format is the same as the ``options`` parameter of the `select()` function
    :param bool inline: Whether to display the options on one line. Default is ``False``
    :param str value: The value of the initial selected items.
       You can also set the initial selected option by setting the ``selected`` field in the ``options`` list item.
    :param bool required: whether to must select one option. (the user can select nothing option by default)
    :param - label, validate, name, onchange, help_text, other_html_attrs: Those arguments have the same meaning as for `input()`
    :return: The value of the option selected by the user, if the user does not select any value, return ``None``
    """
    assert options is not None, 'Required `options` parameter in radio()'

    item_spec, valid_func, onchange_func = _parse_args(locals())
    item_spec['options'] = _parse_select_options(options)
    if value is not None:
        del item_spec['value']
        item_spec['options'] = _set_options_selected(item_spec['options'], value)

    # From https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/required
    # In the case of a same named group of radio buttons, if a single radio button in the group has the required attribute,
    # a radio button in that group must be checked, although it doesn't have to be the one with the attribute is applied
    if required is not None:
        del item_spec['required']
        item_spec['options'][-1]['required'] = required
    item_spec['type'] = RADIO

    return single_input(item_spec, valid_func, lambda d: d, onchange_func)


def _parse_action_buttons(buttons):
    """
    :param label:
    :param actions: action list
        action available format：

        * dict: ``{label:button label, value:button value, [type: button type], [disabled:is disabled?]}``
        * tuple or list: ``(label, value, [type], [disabled])``
        * single value: label and value of button share the same value

    :return: dict format
    """
    act_res = []
    for act in buttons:
        act = copy.deepcopy(act)
        if isinstance(act, Mapping):
            assert 'label' in act, 'actions item must have label key'
            assert 'value' in act or act.get('type', 'submit') != 'submit' or act.get('disabled'), \
                'actions item must have value key for submit type'
        elif isinstance(act, (list, tuple)):
            assert len(act) in (2, 3, 4), 'actions item format error'
            act = dict(zip(('label', 'value', 'type', 'disabled'), act))
        else:
            act = dict(value=act, label=act)

        act.setdefault('type', 'submit')
        assert act['type'] in ('submit', 'reset', 'cancel'), \
            "submit type must be 'submit'/'reset'/'cancel', not %r" % act['type']
        act_res.append(act)

    return act_res


def actions(label: str = '', buttons: List[Union[Dict[str, Any], Tuple, List, str]] = None, name: str = None,
            help_text: str = None):
    r"""Actions selection

    It is displayed as a group of buttons on the page. After the user clicks the button of it,
    it will behave differently depending on the type of the button.

    :param list buttons: list of buttons. The available formats of the list items are:

        * dict::

             {
                "label":(str) button label,
                "value":(object) button value,
                "type":(str, optional) button type,
                "disabled":(bool, optional) whether the button is disabled,
                "color":(str, optional) button color
             }

          When ``type='reset'/'cancel'`` or ``disabled=True``, ``value`` can be omitted
        * tuple or list: ``(label, value, [type], [disabled])``
        * single value: label and value of button use the same value

       The ``value`` of button can be any JSON serializable object.

       ``type`` can be:

        * ``'submit'`` : After clicking the button, the entire form is submitted immediately,
          and the value of this input item in the final form is the ``value`` of the button that was clicked.
          ``'submit'`` is the default value of ``type``
        * ``'cancel'`` : Cancel form. After clicking the button, the entire form will be submitted immediately,
          and the form value will return ``None``
        * ``'reset'`` : Reset form. After clicking the button, the entire form will be reset,
          and the input items will become the initial state.
          Note: After clicking the ``type=reset`` button, the form will not be submitted,
          and the ``actions()`` call will not return

        The ``color`` of button can be one of: `primary`, `secondary`, `success`, `danger`, `warning`, `info`, `light`,
        `dark`.

    :param - label, name, help_text: Those arguments have the same meaning as for `input()`
    :return: If the user clicks the ``type=submit`` button to submit the form,
        return the value of the button clicked by the user.
        If the user clicks the ``type=cancel`` button or submits the form by other means, ``None`` is returned.

    When ``actions()`` is used as the last input item in `input_group()` and contains a button with ``type='submit'``,
    the default submit button of the `input_group()` form will be replace with the current ``actions()``

    **usage scenes of actions() **

    .. _custom_form_ctrl_btn:

    * Perform simple selection operations:

    .. exportable-codeblock::
        :name: actions-select
        :summary: Use `actions()` to perform simple selection

        confirm = actions('Confirm to delete file?', ['confirm', 'cancel'],
                              help_text='Unrecoverable after file deletion')
        if confirm=='confirm':  # ..doc-only
            ...  # ..doc-only
        put_markdown('You clicked the `%s` button' % confirm)  # ..demo-only

    Compared with other input items, when using `actions()`, the user only needs to click once to complete the submission.

    * Replace the default submit button:

    .. exportable-codeblock::
        :name: actions-submit
        :summary: Use `actions()` to replace the default submit button

        import json  # ..demo-only
                     # ..demo-only
        info = input_group('Add user', [
            input('username', type=TEXT, name='username', required=True),
            input('password', type=PASSWORD, name='password', required=True),
            actions('actions', [
                {'label': 'Save', 'value': 'save'},
                {'label': 'Save and add next', 'value': 'save_and_continue'},
                {'label': 'Reset', 'type': 'reset', 'color': 'warning'},
                {'label': 'Cancel', 'type': 'cancel', 'color': 'danger'},
            ], name='action', help_text='actions'),
        ])
        put_code('info = ' + json.dumps(info, indent=4))
        if info is not None:
            save_user(info['username'], info['password'])  # ..doc-only
            if info['action'] == 'save_and_continue':
                add_next()  # ..doc-only
                put_text('Save and add next...')  # ..demo-only

    """
    assert buttons is not None, 'Required `buttons` parameter in actions()'

    item_spec, valid_func, onchange_func = _parse_args(locals())
    item_spec['type'] = 'actions'
    item_spec['buttons'] = _parse_action_buttons(buttons)

    return single_input(item_spec, valid_func, lambda d: d, onchange_func)


def file_upload(label: str = '', accept: Union[List, str] = None, name: str = None, placeholder: str = 'Choose file',
                multiple: bool = False, max_size: Union[int, str] = 0, max_total_size: Union[int, str] = 0,
                required: bool = None, help_text: str = None, **other_html_attrs):
    r"""File uploading

    :param accept: Single value or list, indicating acceptable file types. The available formats of file types are:

        * A valid case-insensitive filename extension, starting with a period (".") character. For example: ``.jpg``, ``.pdf``, or ``.doc``.
        * A valid MIME type string, with no extensions.
          For examples: ``application/pdf``, ``audio/*``, ``video/*``, ``image/*``.
          For more information, please visit: https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types

    :type accept: str or list
    :param str placeholder: A hint to the user of what to be uploaded. It will appear in the input field when there is no file selected.
    :param bool multiple: Whether to allow upload multiple files. Default is ``False``.
    :param int/str max_size: The maximum size of a single file, exceeding the limit will prohibit uploading.
        The default is 0, which means there is no limit to the size.

       ``max_size`` can be a integer indicating the number of bytes, or a case-insensitive string ending with `K` / `M` / `G`
       (representing kilobytes, megabytes, and gigabytes, respectively).
       E.g: ``max_size=500``, ``max_size='40K'``, ``max_size='3M'``

    :param int/str max_total_size: The maximum size of all files. Only available when ``multiple=True``.
        The default is 0, which means there is no limit to the size. The format is the same as the ``max_size`` parameter
    :param bool required: Indicates whether the user must specify a file for the input. Default is ``False``.
    :param - label, name, help_text, other_html_attrs: Those arguments have the same meaning as for `input()`
    :return: When ``multiple=False``, a dict is returned::

        {
            'filename': file name，
            'content'：content of the file (in bytes),
            'mime_type': MIME type of the file,
            'last_modified': Last modified time (timestamp) of the file
        }

       If there is no file uploaded, return ``None``.

       When ``multiple=True``, a list is returned. The format of the list item is the same as the return value when ``multiple=False`` above.
       If the user does not upload a file, an empty list is returned.

    .. note::

        If uploading large files, please pay attention to the file upload size limit setting of the web framework.
        When using :func:`start_server() <pywebio3.platform.tornado.start_server>` or
        :func:`path_deploy() <pywebio3.platform.path_deploy>` to start the PyWebIO application,
        the maximum file size to be uploaded allowed by the web framework can be set through the ``max_payload_size`` parameter.

    .. exportable-codeblock::
        :name: file_upload_example
        :summary: `file_upload()` example

        # Upload a file and save to server                      # ..doc-only
        f = input.file_upload("Upload a file")                  # ..doc-only
        open('asset/'+f['filename'], 'wb').write(f['content'])  # ..doc-only

        imgs = file_upload("Select some pictures:", accept="image/*", multiple=True)
        for img in imgs:
            put_image(img['content'])

    """
    item_spec, valid_func, onchange_func = _parse_args(locals())
    item_spec['type'] = 'file'
    item_spec['max_size'] = parse_file_size(max_size) or platform_setting.MAX_PAYLOAD_SIZE
    item_spec['max_total_size'] = parse_file_size(max_total_size) or platform_setting.MAX_PAYLOAD_SIZE

    if platform_setting.MAX_PAYLOAD_SIZE:
        if item_spec['max_size'] > platform_setting.MAX_PAYLOAD_SIZE or \
                item_spec['max_total_size'] > platform_setting.MAX_PAYLOAD_SIZE:
            raise ValueError('The `max_size` and `max_total_size` value can not exceed the backend payload size limit. '
                             'Please increase the `max_total_size` of `start_server()`/`path_deploy()`')

    return single_input(item_spec, valid_func, lambda d: d, onchange_func)


def slider(label: str = '', *, name: str = None, value: Union[int, float] = 0, min_value: Union[int, float] = 0,
           max_value: Union[int, float] = 100, step: int = 1, validate: Callable[[Any], Optional[str]] = None,
           onchange: Callable[[Any], None] = None, required: bool = None, help_text: str = None, **other_html_attrs):
    r"""Range input.

    :param int/float value: The initial value of the slider.
    :param int/float min_value: The minimum permitted value.
    :param int/float max_value: The maximum permitted value.
    :param int step: The stepping interval.
       Only available when ``value``, ``min_value`` and ``max_value`` are all integer.
    :param - label, name, validate, onchange, required, help_text, other_html_attrs: Those arguments have the same meaning as for `input()`
    :return int/float: If one of ``value``, ``min_value`` and ``max_value`` is float,
       the return value is a float, otherwise an int is returned.
    """
    item_spec, valid_func, onchange_func = _parse_args(locals())
    item_spec['type'] = 'slider'
    item_spec['float'] = any(isinstance(i, float) for i in (value, min_value, max_value))
    if item_spec['float']:
        item_spec['step'] = 'any'

    return single_input(item_spec, valid_func, lambda d: d, onchange_func)


def input_group(
        label: str = '',
        inputs: List = None,
        validate: Callable[[Dict], Optional[Tuple[str, str]]] = None,
        cancelable: bool = False,
):
    """
    输入组。立即向用户请求一组输入。
    :param str label: 输入组的标签。
    :param list inputs: 输入项。列表中的项是对单输入函数的调用，而name参数需要在单输入函数中传递。
    :param callable validate: 组的验证函数。如果提供了验证函数，则在用户提交表单时调用验证函数。

        Function signature: ``callback(data) -> (name, error_msg)``.
        ``validate`` receives the value of the entire group as a parameter. When the form value is valid, it returns ``None``.
        When an input item's value is invalid, it returns the ``name`` value of the item and an error message.
        For example:

    .. exportable-codeblock::
        :name: input_group-valid_func
        :summary: `input_group()` form validation

        def check_form(data):
            if len(data['name']) > 6:
                return ('name', 'Name to long!')
            if data['age'] <= 0:
                return ('age', 'Age cannot be negative!')

        data = input_group("Basic info",[
            input('Input your name', name='name'),
            input('Repeat your age', name='age', type=NUMBER)
        ], validate=check_form)

        put_text(data['name'], data['age'])

    :param bool cancelable: 是否可以取消表格默认为“False”。如果cancelable=True，窗体底部将显示一个Cancel按钮。注意：如果组中的最后一个输入项是actions()， cancelable将被忽略。

    :return: 如果用户取消表单，则返回“None”，否则返回“dict”，其键为输入项的“name”，其值为输入项的值。
    """
    assert inputs is not None, 'Required `inputs` parameter in input_group()'

    spec_inputs = []
    preprocess_funcs = {}
    item_valid_funcs = {}
    onchange_funcs = {}
    for single_input_return in inputs:
        input_kwargs = single_input_kwargs(single_input_return)

        assert all(
            k in (input_kwargs or {})
            for k in ('item_spec', 'preprocess_func', 'valid_func', 'onchange_func')
        ), "`inputs` value error in `input_group`. Did you forget to add `name` parameter in input function?"

        input_name = input_kwargs['item_spec']['name']
        assert input_name, "`name` can not be empty!"
        if input_name in preprocess_funcs:
            raise ValueError('Duplicated input item name "%s" in same input group!' % input_name)
        preprocess_funcs[input_name] = input_kwargs['preprocess_func']
        item_valid_funcs[input_name] = input_kwargs['valid_func']
        onchange_funcs[input_name] = input_kwargs['onchange_func']
        spec_inputs.append(input_kwargs['item_spec'])

    if all('auto_focus' not in i for i in spec_inputs):  # No `auto_focus` parameter is set for each input item
        for i in spec_inputs:
            text_inputs = {TEXT, NUMBER, PASSWORD, SELECT, URL, FLOAT, DATE, TIME, DATETIME_LOCAL}
            if i.get('type') in text_inputs:
                i['auto_focus'] = True
                break

    spec = dict(label=label, inputs=spec_inputs, cancelable=cancelable)
    return input_control(spec, preprocess_funcs=preprocess_funcs,
                         item_valid_funcs=item_valid_funcs,
                         onchange_funcs=onchange_funcs,
                         form_valid_funcs=validate)


def parse_input_update_spec(spec):
    for key in spec:
        assert key not in {'action', 'buttons', 'code', 'inline', 'max_size', 'max_total_size', 'multiple', 'name',
                           'onchange', 'type', 'validate'}, '%r can not be updated' % key

    attributes = dict((k, v) for k, v in spec.items() if v is not None)
    if 'options' in spec:
        attributes['options'] = _parse_select_options(spec['options'])
    return attributes


def input_update(name: str = None, **spec):
    """Update attributes of input field.
    This function can only be called in ``onchange`` callback of input functions.

    :param str name: The ``name`` of the target input item.
       Optional, default is the name of input field which triggers ``onchange``
    :param spec: The input parameters need to be updated.
       Note that those parameters can not be updated:
       ``type``, ``name``, ``validate``, ``action``, ``code``, ``onchange``, ``multiple``

    An example of implementing dependent input items in an input group:

    .. exportable-codeblock::
        :name: input-update
        :summary: Dependent input items in input group

        country2city = {
            'China': ['Beijing', 'Shanghai', 'Hong Kong'],
            'USA': ['New York', 'Los Angeles', 'San Francisco'],
        }
        countries = list(country2city.keys())
        location = input_group("Select a location", [
            select('Country', options=countries, name='country',
                   onchange=lambda c: input_update('city', options=country2city[c])),
            select('City', options=country2city[countries[0]], name='city'),
        ])
        put_text(location)  # ..demo-only
    """
    task_id = get_current_task_id()
    k = 'onchange_trigger-' + task_id
    if k not in get_current_session().internal_save:
        raise RuntimeError("`input_update()` can only be called in `onchange` callback.")
    trigger_name = get_current_session().internal_save[k]

    if name is None:
        name = trigger_name

    attributes = parse_input_update_spec(spec)

    send_msg('update_input', dict(target_name=name, attributes=attributes))
