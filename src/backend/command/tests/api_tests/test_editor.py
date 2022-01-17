from command.tests.common import CommandTestCase
from utils.plane import PlaneEnum
import os


class EditorTest(CommandTestCase):

    def test_workspaces(self):
        name1 = f"{self.__class__.__name__}_test_ws_1"
        name2 = f"{self.__class__.__name__}_test_ws_2"
        with self.app.test_client() as c:
            rv = c.post(f"/AAZ/Editor/Workspaces", json={
                "name": name1,
                "plane": PlaneEnum.Mgmt,
            })
            assert rv.status_code == 200
            ws1 = rv.get_json()
            assert ws1['name'] == name1
            assert ws1['plane'] == PlaneEnum.Mgmt
            assert ws1['version']
            assert ws1['url']
            assert ws1['commandTree']['name'] == 'aaz'
            assert os.path.exists(ws1['folder'])

            rv = c.post(f"/AAZ/Editor/Workspaces", json={
                "name": name2,
                "plane": PlaneEnum.Mgmt,
            })
            assert rv.status_code == 200
            ws2 = rv.get_json()
            assert ws2['name'] == name2
            assert ws2['plane'] == PlaneEnum.Mgmt
            assert ws2['version']
            assert ws2['url']
            assert os.path.exists(ws2['folder'])

            rv = c.get(f"/AAZ/Editor/Workspaces")
            ws_list = rv.get_json()
            assert len(ws_list) == 2
            for ws_data in ws_list:
                if ws_data['name'] == name1:
                    assert ws_data['url'] == ws1['url']
                    assert ws_data['folder'] == ws1['folder']
                elif ws_data['name'] == name2:
                    assert ws_data['url'] == ws2['url']
                    assert ws_data['folder'] == ws2['folder']

            rv = c.post(f"/AAZ/Editor/Workspaces", json={
                "name": name2,
                "plane": PlaneEnum.Mgmt,
            })
            assert rv.status_code == 409

    def test_workspace(self):
        name1 = f"{self.__class__.__name__}_test_ws_1"
        with self.app.test_client() as c:
            rv = c.post(f"/AAZ/Editor/Workspaces", json={
                "name": name1,
                "plane": PlaneEnum.Mgmt,
            })
            assert rv.status_code == 200
            ws = rv.get_json()
            with self.app.test_client() as c:
                rv = c.get(ws['url'])
                assert rv.status_code == 200
                assert rv.get_json() == ws
                rv = c.get(f"/AAZ/Editor/Workspaces/{ws['name']}")
                assert rv.status_code == 200
                assert rv.get_json() == ws

            # with self.app.test_client() as c:
            #     rv = c.put(ws['url'], json=ws)
            #     assert rv.status_code == 200
            #     ws2 = rv.get_json()
            #     assert ws2['version'] != ws['version']

            with self.app.test_client() as c:
                rv = c.delete(ws['url'])
                assert rv.status_code == 200
                rv = c.delete(ws['url'])
                assert rv.status_code == 204
