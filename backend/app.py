from flask import Flask, jsonify, request
from models import db, User, Region
from flask_cors import CORS # 处理跨域
import re  # 导入正则表达式库
from user_routes import register_user_routes
from service_need_routes import register_service_need_routes
from service_response_routes import register_service_response_routes
from admin_routes import register_admin_routes

app = Flask(__name__)
# 允许跨域，这样 Vue 才能访问 Flask
CORS(app)

# 数据库连接配置 (用户名:密码@地址/数据库名)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:963852741zcbm@localhost/good_service_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# 注册所有路由
register_user_routes(app)
register_service_need_routes(app)
register_service_response_routes(app)
register_admin_routes(app)

# 自动创建所有表，并初始化管理员账号
@app.cli.command("init-db")
def init_db():
    db.create_all()
    # 插入默认管理员
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', password='admin', user_type='admin', real_name='系统管理员')
        db.session.add(admin)
        db.session.commit()
    print("数据库初始化完成，管理员 admin 已创建！")

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        phone = data.get('phone')
        
        # 1. 基础非空校验
        if not username or not password:
            return jsonify({"code": 400, "msg": "用户名和密码不能为空"}), 400

        # 2. 密码复杂度校验 (需求要求：不少于6位，含两个数字，不能全大/小写)
        # 长度校验
        if len(password) < 6:
            return jsonify({"code": 400, "msg": "密码长度不能少于6位"}), 400
        
        # 数字个数校验 (查找所有数字，看长度是否 >= 2)
        digits = re.findall(r'\d', password)
        if len(digits) < 2:
            return jsonify({"code": 400, "msg": "密码必须含有至少两个数字"}), 400
        
        # 大小写混杂校验 (不能全是小写 且 不能全是大写)
        if password.islower() or password.isupper():
            return jsonify({"code": 400, "msg": "密码不能全是全大写或全小写"}), 400

        # 3. 检查用户名是否已存在
        if User.query.filter_by(username=username).first():
            return jsonify({"code": 400, "msg": "用户名已被注册"}), 400

        # 4. 写入数据库
        new_user = User(
            username=username,
            password=password,  # 原型系统暂用明文，实际开发建议用 generate_password_hash
            phone=phone,
            user_type='normal'
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"code": 200, "msg": "注册成功"}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Register error: {str(e)}")
        return jsonify({"code": 500, "msg": f"系统错误: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
