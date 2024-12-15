import asyncio
import inspect
import json


class Executor:
    def __init__(self):
        self.heartbeat_interval = 1  # 心跳包发送间隔

    def sayHi(self) -> str:
        print("hi")
        with open("/Users/zhangjinhua/Desktop/LLM-Study/txt.json", 'r', encoding='utf-8-sig') as file:
            # 读取文件内容
            file_content = file.read()
            # 解析为 JSON 对象
            json_data = json.loads(file_content)
            return json_data

    def currentWeather(self, time, day) -> dict:
        return {
            "today": "nice",
            "time": time,
            "day": day
        }

    def current(self) -> list:
        return [{"a": "h"}]


class TCPClient:
    def __init__(self, host='127.0.0.1', port=8888, instance=None, limit=2 ** 20):
        self.host = host
        self.port = port
        self.instance = instance
        self.limit = limit

    async def execute(self):
        while True:
            try:
                await self.connect_server()
            except Exception as e:
                print(f'disconnect from server:{e}')
                await asyncio.sleep(2)

    async def connect_server(self):
        reader, writer = await asyncio.open_connection(self.host, self.port, limit=self.limit)

        try:
            while True:
                # 等待服务器的回复
                data = await reader.readuntil(b'\r\n')
                if data.__len__() == 0:
                    continue
                print(f'Received from server: {data.decode()}')
                request = json.loads(data)

                if request["command"] == "rest-api":
                    result = class_info
                else:
                    method = getattr(self.instance, request["command"])
                    kwargs = request["request"]
                    result = method(**kwargs)

                if result is None:
                    print(f'No response')

                resp = {
                    "id": request["id"],
                    "data": result,
                    "code": 0,
                }

                resp_data = (json.dumps(resp) + '\r\n').encode()
                if resp_data.__len__() > self.limit:
                    resp["code"] = 500
                    resp[
                        "message"] = f"resp data is too large[{resp_data.__len__()}], which is over limit[{self.limit}]"

                writer.write(resp_data)
        except Exception as e:
            print(f"get a exception: {e}")
        finally:
            print('Closing connection')
            writer.close()
            await writer.wait_closed()


def get_class_methods_info(cls):
    methods_info = []
    for name in dir(cls):
        method = getattr(cls, name)
        if callable(method) and not name.startswith("__"):  # 过滤掉私有方法
            # 获取方法的签名
            sig = inspect.signature(method)
            return_annotation = sig.return_annotation
            request = []
            for item in sig.parameters.items():
                if item[0] != "self":
                    request.append(item[0])

            # 记录方法信息
            methods_info.append({
                "path": name,
                "request": request,
                "response": str(return_annotation) if return_annotation is not inspect.Signature.empty else "None",
            })
    return methods_info


class_info = get_class_methods_info(Executor)

if __name__ == "__main__":
    client = TCPClient(instance=Executor())
    asyncio.run(client.execute())
