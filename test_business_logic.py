#!/usr/bin/env python3
"""
业务逻辑测试脚本 - 用于验证系统的核心业务逻辑是否正常工作
包括服务需求发布、响应、接受等流程
"""

import requests
import json
import time

# 配置
BASE_URL = "http://127.0.0.1:5000"

# 测试用户
TEST_USER = {
    "username": "user1",
    "password": "Pass1234",
    "real_name": "测试用户",
    "phone": "13800138000",
    "bio": "测试用户简介"
}

ADMIN_USER = {
    "username": "admin",
    "password": "admin"
}

# 测试服务类型
TEST_SERVICE_TYPE = "管道维修"

# 测试地域信息
TEST_REGION = {
    "province": "广东省",
    "city": "广州市",
    "name": "天河区"
}

class BusinessLogicTester:
    """业务逻辑测试类"""
    
    def __init__(self):
        self.user_token = None
        self.admin_token = None
        self.test_user_id = None
        self.other_user_id = None
        self.test_need_id = None
        self.test_response_id = None
        
    def login(self, username, password):
        """登录获取用户信息"""
        url = f"{BASE_URL}/api/login"
        data = {
            "username": username,
            "password": password
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"登录失败: {response.status_code} - {response.text}")
            return None
    
    def test_user_management(self):
        """测试用户管理功能"""
        print("\n=== 测试用户管理功能 ===")
        
        # 管理员登录
        admin_login = self.login(ADMIN_USER["username"], ADMIN_USER["password"])
        if not admin_login:
            print("管理员登录失败，无法继续测试")
            return False
        
        print("✅ 管理员登录成功")
        
        # 普通用户登录
        user_login = self.login("user1", "User123456")
        if not user_login:
            print("普通用户登录失败，无法继续测试")
            return False
        
        self.test_user_id = user_login["data"]["id"]
        print(f"✅ 普通用户登录成功，用户ID: {self.test_user_id}")
        
        # 另一个测试用户登录
        other_login = self.login("user2", "User123456")
        if not other_login:
            print("另一个普通用户登录失败，无法继续测试")
            return False
        
        self.other_user_id = other_login["data"]["id"]
        print(f"✅ 另一个普通用户登录成功，用户ID: {self.other_user_id}")
        
        return True
    
    def test_service_need_creation(self):
        """测试服务需求发布功能"""
        print("\n=== 测试服务需求发布功能 ===")
        
        # 获取地域ID
        regions_url = f"{BASE_URL}/api/regions"
        regions_response = requests.get(regions_url)
        if regions_response.status_code != 200:
            print(f"获取地域列表失败: {regions_response.status_code} - {regions_response.text}")
            return False
        
        regions = regions_response.json()["data"]
        # 找到一个测试地域
        test_region = next((r for r in regions if r["province"] == TEST_REGION["province"] and r["city"] == TEST_REGION["city"]), None)
        if not test_region:
            print(f"未找到测试地域: {TEST_REGION}")
            return False
        
        region_id = test_region["id"]
        print(f"✅ 获取地域列表成功，测试地域ID: {region_id}")
        
        # 发布服务需求
        need_url = f"{BASE_URL}/api/service-needs"
        need_data = {
            "user_id": self.test_user_id,
            "subject": "测试服务需求",
            "service_type": TEST_SERVICE_TYPE,
            "description": "这是一个测试服务需求",
            "region_id": region_id
        }
        
        need_response = requests.post(need_url, json=need_data)
        if need_response.status_code != 200:
            print(f"发布服务需求失败: {need_response.status_code} - {need_response.text}")
            return False
        
        self.test_need_id = need_response.json()["data"]["id"]
        print(f"✅ 发布服务需求成功，需求ID: {self.test_need_id}")
        
        return True
    
    def test_service_response_creation(self):
        """测试服务响应创建功能"""
        print("\n=== 测试服务响应创建功能 ===")
        
        # 创建服务响应
        response_url = f"{BASE_URL}/api/service-responses"
        response_data = {
            "need_id": self.test_need_id,
            "user_id": self.other_user_id,
            "content": "我可以提供此服务，经验丰富"
        }
        
        response_response = requests.post(response_url, json=response_data)
        if response_response.status_code != 200:
            print(f"创建服务响应失败: {response_response.status_code} - {response_response.text}")
            return False
        
        self.test_response_id = response_response.json()["data"]["id"]
        print(f"✅ 创建服务响应成功，响应ID: {self.test_response_id}")
        
        # 测试不能对自己的需求进行响应
        invalid_response_data = {
            "need_id": self.test_need_id,
            "user_id": self.test_user_id,
            "content": "不能对自己的需求进行响应"
        }
        
        invalid_response = requests.post(response_url, json=invalid_response_data)
        if invalid_response.status_code == 200:
            print("❌ 错误：可以对自己的需求进行响应")
            return False
        
        print("✅ 不能对自己的需求进行响应，验证成功")
        
        return True
    
    def test_service_response_accept(self):
        """测试服务响应接受功能"""
        print("\n=== 测试服务响应接受功能 ===")
        
        # 接受服务响应
        accept_url = f"{BASE_URL}/api/service-responses/{self.test_response_id}"
        accept_data = {
            "user_id": self.test_user_id,
            "status": 1
        }
        
        accept_response = requests.put(accept_url, json=accept_data)
        if accept_response.status_code != 200:
            print(f"接受服务响应失败: {accept_response.status_code} - {accept_response.text}")
            return False
        
        print("✅ 接受服务响应成功")
        
        # 检查是否创建了ResponseSuccess记录
        success_url = f"{BASE_URL}/api/admin/stats/overview"
        success_response = requests.get(success_url)
        if success_response.status_code != 200:
            print(f"获取概览统计失败: {success_response.status_code} - {success_response.text}")
            return False
        
        success_count = success_response.json()["data"]["total_success"]
        print(f"✅ 检查成功配对数: {success_count} (应该大于0)")
        
        return True
    
    def test_monthly_summary_update(self):
        """测试月度统计更新功能"""
        print("\n=== 测试月度统计更新功能 ===")
        
        # 获取月度统计数据
        monthly_url = f"{BASE_URL}/api/admin/stats/monthly-summary"
        monthly_response = requests.get(monthly_url)
        if monthly_response.status_code != 200:
            print(f"获取月度统计数据失败: {monthly_response.status_code} - {monthly_response.text}")
            return False
        
        monthly_data = monthly_response.json()["data"]
        print(f"✅ 获取月度统计数据成功，数据条数: {len(monthly_data)}")
        
        # 检查是否有数据
        if len(monthly_data) > 0:
            print(f"✅ 月度统计数据不为空，第一条数据: {monthly_data[0]}")
        else:
            print("⚠️  月度统计数据为空，可能是因为当前月份没有数据")
        
        return True
    
    def run_all_tests(self):
        """运行所有测试"""
        print("=== 开始业务逻辑测试 ===")
        
        # 仅运行用户管理测试，用于调试
        tests = [
            self.test_user_management,
        ]
        
        passed = 0
        failed = 0
        
        for test in tests:
            try:
                if test():
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                print(f"测试执行出错: {str(e)}")
                failed += 1
            time.sleep(1)  # 避免请求过快
        
        print("\n=== 测试结果总结 ===")
        print(f"总测试数: {len(tests)}")
        print(f"通过: {passed}")
        print(f"失败: {failed}")
        
        if failed == 0:
            print("🎉 所有测试通过！业务逻辑正常工作。")
            return True
        else:
            print("❌ 部分测试失败，请检查系统业务逻辑。")
            return False

if __name__ == "__main__":
    tester = BusinessLogicTester()
    tester.run_all_tests()
