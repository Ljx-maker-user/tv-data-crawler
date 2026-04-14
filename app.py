import pymysql
from flask import Flask, render_template, jsonify

from xiangqing import select

app = Flask(__name__)


@app.route('/')  # 首页，显示电视剧数据
def movies():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/charts')  # 添加charts路由
def charts():
    return render_template('charts.html')

@app.route('/top25')
def top250():
    sql = "SELECT `rank`, name, year, actor, popularity, url  FROM tv ORDER BY `rank`"
    # 执行查询时传入分页参数（防止SQL注入）
    data = select(sql)
    return render_template('top25.html', data=data)

@app.route('/api/movies')  # API接口，返回JSON格式的电影数据
def api_movies():
    db = getDB()
    cursor = db.cursor()
    sql = "SELECT rank, name, year, actor, popularity, url FROM tv ORDER BY rank"
    cursor.execute(sql)
    data = cursor.fetchall()

    dataList = []
    for item in data:
        dataList.append({
            'rank': item[0],
            'name': item[1],
            'year': item[2],
            'actor': item[3],
            'popularity': item[4],
            'url': item[5]
        })

    cursor.close()
    db.close()

    return jsonify(dataList)

@app.route('/api/stats')  # API接口，返回统计数据
def api_stats():
    db = getDB()
    cursor = db.cursor()
    stats = get_stats(cursor)

    cursor.close()
    db.close()

    return jsonify(stats)

def get_stats(cursor):
    # 获取年份分布
    cursor.execute("SELECT year, COUNT(*) FROM tv GROUP BY year ORDER BY year")
    year_data = cursor.fetchall()
    years = [str(item[0]) for item in year_data]
    year_counts = [item[1] for item in year_data]

    # 获取热度分布
    cursor.execute("""
        SELECT 
            CASE 
                WHEN popularity < 10000 THEN '1万以下'
                WHEN popularity BETWEEN 10000 AND 20000 THEN '1-2万'
                WHEN popularity BETWEEN 20000 AND 30000 THEN '2-3万'
                WHEN popularity BETWEEN 30000 AND 40000 THEN '3-4万'
                WHEN popularity BETWEEN 40000 AND 50000 THEN '4-5万'
                ELSE '5万以上'
            END as pop_range,
            COUNT(*) 
        FROM tv 
        GROUP BY pop_range 
        ORDER BY MIN(popularity)
    """)
    pop_data = cursor.fetchall()
    pop_ranges = [item[0] for item in pop_data]
    pop_counts = [item[1] for item in pop_data]

    # 获取主演统计（简化版）
    cursor.execute("SELECT actor FROM tv")
    actors_data = cursor.fetchall()

    # 简单的演员统计（实际应用中可能需要更复杂的处理）
    actor_count = {}
    for item in actors_data:
        actors = item[0].split()
        for actor in actors:
            if actor in actor_count:
                actor_count[actor] += 1
            else:
                actor_count[actor] = 1

    # 取作品数量前6的演员
    sorted_actors = sorted(actor_count.items(), key=lambda x: x[1], reverse=True)[:6]
    top_actors = [item[0] for item in sorted_actors]
    actor_counts = [item[1] for item in sorted_actors]

    return {
        'years': years,
        'year_counts': year_counts,
        'pop_ranges': pop_ranges,
        'pop_counts': pop_counts,
        'top_actors': top_actors,
        'actor_counts': actor_counts
    }

def getDB():
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='2636023',
                         database='dsj',
                         charset='utf8mb4')
    return db

if __name__ == '__main__':
    app.run(debug=True)
