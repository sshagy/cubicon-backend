import logging.config
import datetime
from typing import *

from rest_framework.exceptions import ValidationError
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.routers import APIRootView

# отключение частичного обновления PATCH, которое
# никем не использовалось и захламляло документацию.
# TODO: собрать с фронтов инфу, где они используют метод PATCH, пока не удаляем метод.
from rest_framework.viewsets import ViewSet

if hasattr(UpdateModelMixin, 'partial_update') and 0:
    logging.log(logging.DEBUG, 'Remove `partial_update` from `UpdateModelMixin`')
    del UpdateModelMixin.partial_update


def get_api_navigation(urlpatterns: List['RoutePattern'], pattern: str = None) -> Dict[str, str]:
    view_key_func = lambda p: p.app_name if hasattr(p, 'app_name') else f'_{p.name}'
    view_name_func = lambda p: f'{p.namespace}:api-root' if hasattr(p, 'app_name') else p.name

    def safe_reverse(p: 'RoutePattern') -> str:
        try:
            return reverse(view_name_func(p))
        except Exception as e:
            return ''
    print(222, {
        view_key_func(p): view_name_func(p)
        for p in urlpatterns
        if pattern is None or pattern in safe_reverse(p)
    })
    return {
        view_key_func(p): view_name_func(p)
        for p in urlpatterns
        if pattern is None or pattern in safe_reverse(p)
    }


def get_api_root_view_cls(verbose_name: str) -> Type[Type['APIRootView']]:
    return type('APIRootView', (APIRootView,), {'name': verbose_name})


def get_api_root_view(api_root_dict: Dict, verbose_name: str):
    cls = get_api_root_view_cls(verbose_name)
    return cls.as_view(api_root_dict=api_root_dict)


def get_navigation_data(viewset, app_name: str, kwargs: dict = None) -> dict:
    """Get navigation data.

    Returns:
         {url_name: url, ...}
    """
    kwargs = kwargs or {'pk': ':id'}
    viewset.basename = f'{app_name}:{viewset.basename}'
    return {
        view.url_name: viewset.reverse_action(
            view.url_name,
            kwargs=kwargs if view.detail else None)
        for view in viewset.get_extra_actions()
    }


class AboutViewSet(ViewSet):
    """Вьюсет отображения информации о системе"""
    authentication_classes = ()
    permission_classes = ()
    _RUNSERVER_DATETIME = datetime.datetime.now()

    def version(self, request: 'Request'):
        """Информация о ревизии и ветке с которой собран инстанс"""
        try:
            import git
            repository = git.Repo('./')
        except Exception as e:
            # в случае если не нет доступа к git-репозиторию, возвращаем ошибку.
            raise ValidationError({'error': f'{type(e).__name__}: {str(e)}'})

        return Response({
            **self._get_commit_info(repository),
            # **self._get_versions(request, repository),
            # **self._get_language_info(request),
            **self._get_time_info(),
        })

    # TODO: move to service layer
    def _get_commit_info(self, repository):
        from git.refs.remote import RemoteReference

        commit = repository.commit()
        rev, branch = commit.name_rev.split()  # invalid branch name

        branches = {r.commit.hexsha: r.name for r in repository.references if
                    isinstance(r, RemoteReference)}
        # rev = commit.hexsha
        # branch = branches.get(rev)

        return {
            'revision': rev,
            "branch": branch,  # invalid branch
            "_branch": branches.get(rev),
            "date": str(commit.committed_datetime),
            "author": commit.author.name,
            "message": commit.message,  # summary,
        }

    def _get_time_info(self):
        return {
            "runserver_time": str(self._RUNSERVER_DATETIME),
            "server_uptime": str(datetime.datetime.now() - self._RUNSERVER_DATETIME),
        }


def get_closest_tag(repo, commit=None) -> Text:
    """Возвращает значение ближайщего тега для коммита.
    Если тег стоит на коммите то возвращает просто его название,
    если тег отстает от коммита, то к нему добавляется `+`."""
    commit = commit or repo.commit()
    lc = (c.hexsha for c in repo.iter_commits())
    # todo: remove others tags with 'us', 'dev' words!!!
    tags = {t.commit.hexsha: t for t in repo.tags if 'us' not in t.name and 'dev' not in t.name}

    tag = None
    for c_hexsha in lc:
        if tag:
            break
        for t_hexsha, t in tags.items():
            if not tag and t_hexsha == c_hexsha:
                tag = t
                break
    if tag:
        is_plus = (tag.commit.hexsha != commit.hexsha)
        tag = f'{tag}{["", "+"][is_plus]}'

    return tag