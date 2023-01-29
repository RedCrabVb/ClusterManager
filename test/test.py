import cm.api
import cm.model
import cm.db


def test_add_host():
    host = cm.model.Host
    host.username = 'root'
    host.password = '1234'
    host.hostname = 'vivt.ru'
    print(cm.db.db['hosts'])
    cm.api.add_host(host)
    print(cm.db.db['hosts'])
    assert cm.db.db['hosts'].__sizeof__() >= 0, "Хост должен быть добавлен в память"


if __name__ == '__main__':
    test_add_host()
