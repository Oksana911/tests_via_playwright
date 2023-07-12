from components.page_factory.component import Component


class Table(Component):
    @property
    def type_of(self) -> str:
        return 'table'


class TableBody(Component):
    @property
    def type_of(self) -> str:
        return 'table body'


class TableHead(Component):
    @property
    def type_of(self) -> str:
        return 'table head'
