from flask import jsonify, request
from models import db, User, ServiceNeed, ServiceResponse, Region, ResponseSuccess, MonthlySummary
from sqlalchemy import and_, or_
import re
from datetime import datetime

def register_user_routes(app):
    """注册用户相关的路由"""
    
    @app.route('/api/login', methods=['POST'])
    def login():
        """用户登录"""
        try:
            data = request.json
            username = data.get('username')
            password = data.get('password')
            
            if not username or not password:
                return jsonify({"code": 400, "msg": "用户名和密码不能为空"}), 400
            
            user = User.query.filter_by(username=username, password=password).first()
            if not user:
                return jsonify({"code": 401, "msg": "用户名或密码错误"}), 401
            
            return jsonify({
                "code": 200,
                "msg": "登录成功",
                "data": {
                    "id": user.id,
                    "username": user.username,
                    "real_name": user.real_name,
                    "user_type": user.user_type,
                    "phone": user.phone,
                    "bio": user.bio
                }
            }), 200
        except Exception as e:
            print(f"Login error: {str(e)}")
            return jsonify({"code": 500, "msg": f"系统错误: {str(e)}"}), 500
    
    @app.route('/api/user/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        """获取用户信息"""
        try:
            user = User.query.get(user_id)
            if not user:
                return jsonify({"code": 404, "msg": "用户不存在"}), 404
            
            return jsonify({
                "code": 200,
                "data": {
                    "id": user.id,
                    "username": user.username,
                    "real_name": user.real_name,
                    "user_type": user.user_type,
                    "phone": user.phone,
                    "bio": user.bio,
                    "created_at": user.created_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            }), 200
        except Exception as e:
            return jsonify({"code": 500, "msg": f"系统错误: {str(e)}"}), 500
    
    @app.route('/api/user/<int:user_id>', methods=['PUT'])
    def update_user(user_id):
        """更新用户信息"""
        try:
            data = request.json
            user = User.query.get(user_id)
            if not user:
                return jsonify({"code": 404, "msg": "用户不存在"}), 404
            
            # 只能修改：电话、简介
            if 'phone' in data:
                user.phone = data['phone']
            
            if 'bio' in data:
                user.bio = data['bio']
            
            user.updated_at = datetime.now()
            db.session.commit()
            return jsonify({"code": 200, "msg": "更新成功"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"code": 500, "msg": f"系统错误: {str(e)}"}), 500
    
    @app.route('/api/user/<int:user_id>/password', methods=['PUT'])
    def change_password(user_id):
        """修改密码"""
        try:
            data = request.json
            user = User.query.get(user_id)
            if not user:
                return jsonify({"code": 404, "msg": "用户不存在"}), 404
            
            old_password = data.get('old_password')
            new_password = data.get('new_password')
            
            if not old_password or not new_password:
                return jsonify({"code": 400, "msg": "原密码和新密码不能为空"}), 400
            
            if user.password != old_password:
                return jsonify({"code": 400, "msg": "原密码错误"}), 400
            
            # 校验新密码复杂度
            if len(new_password) < 6:
                return jsonify({"code": 400, "msg": "密码长度不能少于6位"}), 400
            
            digits = re.findall(r'\d', new_password)
            if len(digits) < 2:
                return jsonify({"code": 400, "msg": "密码必须含有至少两个数字"}), 400
            
            if new_password.islower() or new_password.isupper():
                return jsonify({"code": 400, "msg": "密码不能全是大写或小写"}), 400
            
            user.password = new_password
            user.updated_at = datetime.now()
            db.session.commit()
            return jsonify({"code": 200, "msg": "修改成功"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"code": 500, "msg": f"系统错误: {str(e)}"}), 500
    
    @app.route('/api/regions', methods=['GET'])
    def get_regions():
        """获取所有地域信息"""
        try:
            regions = Region.query.all()
            return jsonify({
                "code": 200,
                "data": [{
                    "id": r.id,
                    "name": r.name,
                    "city": r.city,
                    "province": r.province,
                    "full_name": f"{r.province}-{r.city}-{r.name}"
                } for r in regions]
            }), 200
        except Exception as e:
            return jsonify({"code": 500, "msg": f"系统错误: {str(e)}"}), 500
    
    @app.route('/api/user/<int:user_id>/service-needs', methods=['GET'])
    def get_user_service_needs(user_id):
        """获取用户发布的服务需求"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)
            
            user = User.query.get(user_id)
            if not user:
                return jsonify({"code": 404, "msg": "用户不存在"}), 404
            
            query = ServiceNeed.query.filter_by(user_id=user_id)
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)
            
            items = []
            for need in pagination.items:
                region = Region.query.get(need.region_id) if need.region_id else None
                items.append({
                    "id": need.id,
                    "subject": need.subject,
                    "service_type": need.service_type,
                    "description": need.description,
                    "region": f"{region.province}-{region.city}-{region.name}" if region else '未指定',
                    "status": need.status,
                    "created_at": need.created_at.strftime('%Y-%m-%d %H:%M:%S')
                })
            
            return jsonify({
                "code": 200,
                "data": items,
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": pagination.total,
                    "pages": pagination.pages
                }
            }), 200
        except Exception as e:
            return jsonify({"code": 500, "msg": f"系统错误: {str(e)}"}), 500
    
    @app.route('/api/user/<int:user_id>/responses', methods=['GET'])
    def get_user_responses(user_id):
        """获取用户提交的服务响应"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)
            
            user = User.query.get(user_id)
            if not user:
                return jsonify({"code": 404, "msg": "用户不存在"}), 404
            
            query = ServiceResponse.query.filter_by(user_id=user_id)
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)
            
            items = []
            for response in pagination.items:
                need = ServiceNeed.query.get(response.need_id)
                items.append({
                    "id": response.id,
                    "need_subject": need.subject if need else '未知',
                    "content": response.content,
                    "status": response.status,
                    "created_at": response.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    "review_time": response.updated_at.strftime('%Y-%m-%d %H:%M:%S') if response.updated_at else None
                })
            
            return jsonify({
                "code": 200,
                "data": items,
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": pagination.total,
                    "pages": pagination.pages
                }
            }), 200
        except Exception as e:
            return jsonify({"code": 500, "msg": f"系统错误: {str(e)}"}), 500
