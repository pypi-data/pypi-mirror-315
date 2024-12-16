from .base import AbstractPipelinePlugin


class PipelinePluginLoader:
    def process_item(self, item, spider):
        """
        Process an item by calling the process_item method of all
        pipeline plugins returned by the spider's helpers.

        This is a convenience method to simplify the process of calling
        the process_item method of each pipeline plugin. It takes an item
        and a spider instance as arguments and returns the processed item.

        Parameters
        ----------
        item : Item
            The item to be processed.
        spider : Spider
            The spider instance that scraped the item.

        Returns
        -------
        Item
            The processed item.
        """
        for plugin in spider.helpers.get_plugins():
            pipeline_class = plugin.get_pipeline_class()
            if pipeline_class:
                assert issubclass(pipeline_class,
                                  AbstractPipelinePlugin), "Pipeline plugin must be a subclass of AbstractPipelinePlugin"
                item = pipeline_class(item, spider).process_item()
        return item
