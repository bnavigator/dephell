from pip._internal.download import PipSession
from pip._internal.req import parse_requirements
from .models import Dependency, RootDependency
from .controllers import Graph, Mutator, Resolver
from .repositories import WareHouseRepo


Dependency.repo = WareHouseRepo()


def from_requirements(path):
    deps = []
    root = RootDependency()
    for req in parse_requirements(str(path), session=PipSession()):
        deps.append(Dependency.from_requirement(root, req.req))
    root.attach_dependencies(deps)
    graph = Graph(root)
    return Resolver(
        graph=graph,
        mutator=Mutator()
    )
