# 抓取.py (修改后)
import random
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


def draw_lots(groups):
    """
    抓阄程序：从给定的组列表中随机抽取，每组都会被抽取一次且不重复，最后排序

    参数:
    groups: 列表，包含所有组的名称或标识

    返回:
    排序后的抓阄结果列表，每个元素为(序号, 组名)
    """
    # 复制一份组列表，避免修改原列表
    remaining_groups = groups.copy()
    result = []

    # 随机抽取直到所有组都被抽完
    while remaining_groups:
        # 随机选择一个组
        selected = random.choice(remaining_groups)
        # 从剩余组中移除已选择的组
        remaining_groups.remove(selected)
        # 添加到结果列表
        result.append(selected)

    # 为结果添加序号并返回
    return list(enumerate(result, 1))


@app.route('/')
def index():
    """显示抓阄页面"""
    return render_template('draw_lots.html')


@app.route('/draw', methods=['POST'])
def draw():
    """处理抓阄请求"""
    try:
        # 获取前端发送的组数据
        data = request.get_json()
        groups = data.get('groups', [])

        if not groups:
            # 如果没有提供组，使用默认的16个组
            groups = [f"第{i}组" for i in range(1, 17)]

        # 执行抓阄
        result = draw_lots(groups)

        # 格式化结果
        formatted_result = [{"order": order, "group": group} for order, group in result]

        return jsonify({
            "success": True,
            "result": formatted_result,
            "message": "抓阄成功！"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"抓阄过程中出现错误: {str(e)}"
        })


if __name__ == "__main__":
    app.run(debug=True)