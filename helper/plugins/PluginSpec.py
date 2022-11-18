import pluggy

hookspec = pluggy.HookspecMarker("hooks")
hookimpl = pluggy.HookimplMarker("hooks")


class PluginSpec:
    """A hook specification namespace."""

    @hookspec
    def before_all(self, context):
        """My special little hook that you can customize."""

    @hookspec
    def after_all(self, context):
        """My special little hook that you can customize."""

    @hookspec
    def before_scenario(self, context, scenario):
        """My special little hook that you can customize."""

    @hookspec
    def after_scenario(self, context, scenario):
        """My special little hook that you can customize."""

    @hookspec
    def after_feature(self, context, feature):
        """My special little hook that you can customize."""

    @hookspec
    def before_feature(self, context, feature):
        """My special little hook that you can customize."""

    @hookspec
    def after_step(self, context, step):
        """My special little hook that you can customize."""

    @hookspec
    def before_step(self, context, step):
        """My special little hook that you can customize."""

    @hookspec
    def after_tag(self, context, tag):
        """My special little hook that you can customize."""

    @hookspec
    def before_tag(self, context, tag):
        """My special little hook that you can customize."""
