import os
from werkzeug.utils import secure_filename
from flask import current_app
from flask import jsonify, request
from models import db, ServiceNeed, Region, User
from sqlalchemy import and_, desc
from datetime import datetime
from functools import wraps

def require_login(f):
    """装饰器：检查用户是否登录"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = request.headers.get('X-User-ID')
        if not user_id:
            return jsonify({"code": 401, "msg": "未登录"}), 401
        return f(*args, **kwargs)
    return decorated_function

def register_service_need_routes(app):
    """注册"我需要"相关的路由"""
    
    @app.route('/api/service-needs', methods=['GET'])
    def get_service_needs():
        """获取所有服务需求列表（分页）"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)
            service_type = request.args.get('service_type', '')
            region_id = request.args.get('region_id', '', type=int)
            
            query = ServiceNeed.query.filter_by(status=0)
            
            if service_type:
                query = query.filter(ServiceNeed.service_type.contains(service_type))
            
            if region_id:
                query = query.filter(ServiceNeed.region_id == region_id)
            
            # 按创建时间倒序
            query = query.order_by(desc(ServiceNeed.created_at))
            
            # 分页
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)
            
            items = []
            for need in pagination.items:
                user = User.query.get(need.user_id)
                region_obj = Region.query.get(need.region_id) if need.region_id else None
                items.append({
                    "id": need.id,
                    "subject": need.subject,
                    "service_type": need.service_type,
                    "description": need.description[:100] if need.description else '',
                    "region": f"{region_obj.province}-{region_obj.city}-{region_obj.name}" if region_obj else '未指定',
                    "publisher": user.real_name or user.username,
                    "created_at": need.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    "status": need.status,
                    "media_url": need.media_url  
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
    
    @app.route('/api/service-needs/<int:need_id>', methods=['GET'])
    def get_service_need(need_id):
        """获取单个服务需求详情"""
        try:
            need = ServiceNeed.query.get(need_id)
            if not need:
                return jsonify({"code": 404, "msg": "需求不存在"}), 404
            
            user = User.query.get(need.user_id)
            region = Region.query.get(need.region_id) if need.region_id else None
            
            return jsonify({
                "code": 200,
                "data": {
                    "id": need.id,
                    "subject": need.subject,
                    "service_type": need.service_type,
                    "description": need.description,
                    "media_url": need.media_url,
                    "region_id": need.region_id,
                    "region": f"{region.province}-{region.city}-{region.name}" if region else '未指定',
                    "publisher_id": user.id,
                    "publisher": user.real_name or user.username,
                    "publisher_phone": user.phone,
                    "publisher_bio": user.bio,
                    "created_at": need.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    "status": need.status
                }
            }), 200
        except Exception as e:
            return jsonify({"code": 500, "msg": f"系统错误: {str(e)}"}), 500
    
    @app.route('/api/my-service-needs/<int:user_id>', methods=['GET'])
    def get_my_service_needs(user_id):
        """获取当前用户发布的所有需求"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)
            
            query = ServiceNeed.query.filter_by(user_id=user_id).order_by(desc(ServiceNeed.created_at))
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)
            
            items = []
            for need in pagination.items:
                region = Region.query.get(need.region_id) if need.region_id else None
                
                # 查询该需求下的所有响应 
                from models import ServiceResponse, User as UserModel
                responses_data = []
                responses = ServiceResponse.query.filter_by(need_id=need.id).all()
                for resp in responses:
                    resp_user = UserModel.query.get(resp.user_id)
                    responses_data.append({
                        "id": resp.id,
                        "content": resp.content,
                        "media_url": resp.media_url,  
                        "status": resp.status,
                        "responder_name": resp_user.real_name or resp_user.username if resp_user else "未知用户"
                    })
                # ----------------------------------

                items.append({
                    "id": need.id,
                    "subject": need.subject,
                    "service_type": need.service_type,
                    "description": need.description[:100] if need.description else '',
                    "region": f"{region.province}-{region.city}-{region.name}" if region else '未指定',
                    "created_at": need.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    "status": need.status,
                    "media_url": need.media_url,  #发布者自己的图片/视频
                    "status_text": "已发布" if need.status == 0 else "已取消",
                    "responses": responses_data   
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
    
    @app.route('/api/service-needs', methods=['POST'])
    def create_service_need():
        """创建新的服务需求 (支持图片/视频上传)"""
        try:
            # 用 form 获取数据，因为前端传的是 FormData
            user_id = request.form.get('user_id')
            subject = request.form.get('subject')
            service_type = request.form.get('service_type')
            description = request.form.get('description')
            region_id = request.form.get('region_id')
            
            #处理文件上传
            media_url = ''
            if 'file' in request.files:
                file = request.files['file']
                if file and file.filename != '':
                    # 给文件名加个时间戳，防止重名
                    filename = secure_filename(f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}")
                    # 保存到 app.py 里配置好的 uploads 文件夹
                    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                    # 生成访问路径存数据库
                    media_url = f"/uploads/{filename}"

            if not all([user_id, subject, service_type]):
                return jsonify({"code": 400, "msg": "必填字段不能为空"}), 400
            
            need = ServiceNeed(
                user_id=user_id,
                subject=subject,
                service_type=service_type,
                description=description,
                region_id=region_id,
                media_url=media_url,  #把路径存入数据库
                status=0
            )
            
            db.session.add(need)
            db.session.commit()
            
            return jsonify({"code": 200, "msg": "需求发布成功"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"code": 500, "msg": f"系统错误: {str(e)}"}), 500
    
    @app.route('/api/service-needs/<int:need_id>', methods=['PUT'])
    def update_service_need(need_id):
        """修改服务需求"""
        try:
            data = request.json
            need = ServiceNeed.query.get(need_id)
            
            if not need:
                return jsonify({"code": 404, "msg": "需求不存在"}), 404
            
            # 检查权限：只有发布者能修改
            user_id = data.get('user_id')
            if need.user_id != user_id:
                return jsonify({"code": 403, "msg": "无权修改此需求"}), 403
            
            # 只有未响应的需求才能修改
            from models import ServiceResponse
            if ServiceResponse.query.filter_by(need_id=need_id, status=1).first():
                return jsonify({"code": 400, "msg": "已有响应被接受，无法修改"}), 400
            
            # 更新字段
            if 'subject' in data:
                need.subject = data['subject']
            if 'service_type' in data:
                need.service_type = data['service_type']
            if 'description' in data:
                need.description = data['description']
            if 'region_id' in data:
                need.region_id = data['region_id']
            
            need.updated_at = datetime.now()
            db.session.commit()
            
            return jsonify({"code": 200, "msg": "更新成功"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"code": 500, "msg": f"系统错误: {str(e)}"}), 500
    
    @app.route('/api/service-needs/<int:need_id>', methods=['DELETE'])
    def delete_service_need(need_id):
        """删除服务需求"""
        try:
            data = request.json
            need = ServiceNeed.query.get(need_id)
            
            if not need:
                return jsonify({"code": 404, "msg": "需求不存在"}), 404
            
            # 检查权限
            user_id = data.get('user_id')
            if need.user_id != user_id:
                return jsonify({"code": 403, "msg": "无权删除此需求"}), 403
            
            # 只有未响应的需求才能删除
            from models import ServiceResponse
            if ServiceResponse.query.filter_by(need_id=need_id, status=1).first():
                return jsonify({"code": 400, "msg": "已有响应被接受，无法删除"}), 400
            
            # 标记为已取消而不是删除
            need.status = -1
            need.updated_at = datetime.now()
            db.session.commit()
            
            return jsonify({"code": 200, "msg": "删除成功"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"code": 500, "msg": f"系统错误: {str(e)}"}), 500
    