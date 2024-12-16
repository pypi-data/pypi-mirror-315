from typing import Type


class AbstractPipelinePlugin:

    def __init__(self, item, spider):
        self.item = item
        self.spider = spider
        self.crawler_service = spider.crawler_service
        self.helpers = spider.helpers

    @property
    def crawl_request(self):
        return self.crawler_service.crawl_request

    @property
    def plugin_inputs(self):
        return self.crawl_request.options.get('plugin_options', {})

    def process_item(self):
        """
        Process a scraped item through the pipeline.

        This method should be implemented by subclasses to define how the
        scraped `item` should be processed or transformed using the context
        provided by the `spider`.

        Parameters:
        item (ScrapedItem): The item scraped by the spider, containing fields
                            to be processed.
        spider (SiteScrapper): The spider instance that scraped the item, providing
                               additional context if necessary.

        Returns:
        ScrapedItem: The processed item, potentially modified or enhanced.

        Raises:
        NotImplementedError: If the method is not implemented by a subclass.
        """
        raise NotImplementedError


class AbstractInputValidator:

    def __init__(self, crawler_service):
        self.crawler_service = crawler_service
        self.helpers = crawler_service.config_helpers
        self.errors = {}

    @property
    def crawl_request(self):
        return self.crawler_service.crawl_request

    @property
    def plugin_inputs(self):
        return self.crawl_request.options.get('plugin_options', {})

    def add_error(self, field, message):
        if field not in self.errors:
            self.errors[field] = []
        self.errors[field].append(message)

    def is_valid(self):
        try:
            self.validate()
        except Exception as e:
            self.errors["plugin_error"] = [str(e)]
            return False
        return True

    def validate(self):
        """
        Validate the input data for the plugin.

        This method should be implemented by subclasses to define how the input
        data should be validated. It should raise an exception or add errors to
        the `errors` dictionary if the input is invalid.

        The method should not return anything.

        Raises:
        ValueError: If the input data is invalid.
        """
        pass


class AbstractPlugin:

    @classmethod
    def get_pipeline_class(cls) -> Type[AbstractPipelinePlugin] or None:
        """Returns the class of a pipeline plugin to be used by the plugin or None

        If a subclass of AbstractPlugin overrides this method, it should return a
        class that is a subclass of AbstractPipelinePlugin. That class will be used
        by the plugin to process the scraped items.

        If this method is not overridden, it will return None, which means that
        the plugin will not use a pipeline plugin to process the scraped items.
        """
        return None

    @classmethod
    def get_input_validator(cls) -> Type[AbstractInputValidator]:
        """
        Returns the class of an input validator to be used by the plugin.

        If a subclass of AbstractPlugin overrides this method, it should return a
        class that is a subclass of AbstractInputValidator. That class will be used
        by the plugin to validate input data.

        Returns:
        Type[AbstractInputValidator]: The class of the input validator.
        """
        return AbstractInputValidator

    @classmethod
    def extended_fields(cls):
        return []

    @classmethod
    def get_author(cls) -> str:
        raise NotImplementedError

    @classmethod
    def get_version(cls) -> str:
        raise NotImplementedError

    @classmethod
    def get_name(cls) -> str:
        return cls.__name__

    @classmethod
    def get_description(cls) -> str:
        return cls.__doc__
