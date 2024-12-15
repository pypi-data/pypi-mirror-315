import shutil
from datetime import datetime
from zoneinfo import ZoneInfo
from django.utils import timezone
from tests.__init__ import *
from psplpy.django_utils import *


def test_database():
    db = Database(engine=DbBackend.POSTGRESQL, name=get_env('DB_USER'), host=get_env('DB_HOST'), port=get_env('DB_PORT'),
                  user=get_env('DB_USER'), password=get_env('DB_PW'), TIME_ZONE='UTC')
    assert timezone.get_current_timezone() == ZoneInfo('UTC')

    class Test(db.Model):
        name = models.CharField(max_length=200, null=True)
        email = models.EmailField(null=True)
        time = models.DateTimeField(default=timezone.now())

    Test.init()

    naive_time = datetime(2020, 1, 1, 0, 0)
    aware_time = timezone.make_aware(naive_time)
    print(naive_time, aware_time)

    test = Test(name='me', email='test@test.com', time=aware_time)
    test.save()

    all_values = [list(item.values()) for item in Test.objects.all().values()]
    print(all_values)
    assert all_values[0] == [1, 'me', 'test@test.com', aware_time]


def test_django_init():
    def _template(name: str) -> str:
        return (rc_path / 'test' / name).read_text(encoding='utf-8')

    def _modified(name: str) -> str:
        return (tmp_path / 'test' / name).read_text(encoding='utf-8')

    rc_path = rc_dir / 'django_utils'
    tmp_path = tmp_dir / 'django_utils'
    if tmp_path.exists():
        shutil.rmtree(tmp_path)
    shutil.copytree(rc_path, tmp_path)

    # test idempotent
    for _ in range(10):
        di = DjangoInit(project_dir=tmp_path, database=DbBackend.POSTGRESQL).init()
        assert _modified('settings.py') == _template('settings_init.py')
    for _ in range(10):
        di.set_asgi()
        assert _modified('settings.py') == _template('settings_asgi.py')
        assert _modified('asgi.py') == _template('asgi_asgi.py')


def tests():
    test_database()
    test_django_init()


if __name__ == '__main__':
    tests()
