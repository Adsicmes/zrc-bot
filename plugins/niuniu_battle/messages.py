"""牛牛大作战：发送给用户的文案模板（string.Template），每项为数组，回复时随机抽取。"""

from utils import MsgTemplates

# 权限与开关
NEED_ADMIN = MsgTemplates.create("需要管理员权限。")
GROUP_ENABLED = MsgTemplates.create("本群已开启牛牛大作战。")
GROUP_DISABLED = MsgTemplates.create("本群已关闭牛牛大作战。")

# 查看 / 设置 格式提示
VIEW_NEED_AT = MsgTemplates.create("请 @ 要查看的用户。")
SET_FORMAT_EXAMPLE = MsgTemplates.create("格式错误，正确示例：设置牛牛@某人 长度 10.50")

# 导
DAO_RESULT = MsgTemplates.create(
    "导了一下，牛牛长度从 $old_len cm 变成了 $new_len cm。",
    "导完了，牛牛从 $old_len cm 变成 $new_len cm 了。",
)

# 日
RI_SELF_FORBIDDEN = MsgTemplates.create(
    "不能日自己，想改自己的长度请用【导】指令。",
)
RI_RANDOM_FAIL = MsgTemplates.create("暂时无法随机到人。")
RI_NO_TARGET = MsgTemplates.create(
    "群内没有可日的对象。",
    "暂时没有可日的对象。",
)
RI_RESULT = MsgTemplates.create(
    "日了一下，对方的牛牛长度变成了 $new_len cm。",
    "日完了，对方牛牛现在是 $new_len cm。",
)

# 我的牛牛
MY_LENGTH = MsgTemplates.create(
    "你的牛牛长度是 $length cm。",
    "当前牛牛长度：$length cm。",
)

# 查看牛牛@某人
VIEW_OTHER = MsgTemplates.create(
    "该用户牛牛长度：$length cm（尚未参与则显示初始长度 $initial cm）。",
)

# 排行榜
RANK_EMPTY = MsgTemplates.create("本群暂无牛牛数据。")
RANK_TOP_HEADER = MsgTemplates.create("【前十（最长）】")
RANK_BOTTOM_HEADER = MsgTemplates.create("【后十（最短）】")
RANK_LINE = MsgTemplates.create("$rank. QQ $user_id: $length cm")

# 设置牛牛 - 校验与结果
SET_LENGTH_NOT_NUMBER = MsgTemplates.create("长度必须是数字。")
SET_LENGTH_OUT_OF_RANGE = MsgTemplates.create("长度需在 $min 到 $max 之间。")
SET_LENGTH_OK = MsgTemplates.create(
    "已将该用户长度设为 $value cm。",
    "长度已更新为 $value cm。",
)
SET_COUNT_NOT_INT = MsgTemplates.create("设了次数必须是整数。")
SET_COUNT_NEGATIVE = MsgTemplates.create("设了次数不能为负数。")
SET_COUNT_OK = MsgTemplates.create(
    "已将该用户当日设了次数设为 $value。",
    "当日设了次数已更新为 $value。",
)
SET_UNKNOWN_KEY = MsgTemplates.create("未知键【$key】，支持的键：长度、设了次数。")
