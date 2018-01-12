from datetime import timezone

from factory import (
    DjangoModelFactory,
    Faker,
    Trait,
    LazyAttribute,
    post_generation,
)

from networkapi.utility.faker_providers import ImageProvider
from networkapi.highlights.models import Highlight

Faker.add_provider(ImageProvider)


class HighlightFactory(DjangoModelFactory):
    class Meta:
        model = Highlight
        exclude = (
            'title_sentence',
            'description_paragraphs',
            'link_label_words',
            'footer_sentence',
        )

    class Params:
        unpublished = Trait(
            publish_after=Faker(
                'future_datetime',
                end_date='+30d',
                tzinfo=timezone.utc
            )
        )
        has_expiry = Trait(
            expires=Faker(
                'future_datetime',
                end_date='+30d',
                tzinfo=timezone.utc
            )
        )
        expired = Trait(
            expires=Faker(
                'past_datetime',
                start_date='-30d',
                tzinfo=timezone.utc
            )
        )

    title = LazyAttribute(lambda o: o.title_sentence.rstrip('.'))
    description = LazyAttribute(lambda o: ' '.join(o.description_paragraphs))
    link_label = LazyAttribute(lambda o: ' '.join(o.link_label_words))
    footer = LazyAttribute(lambda o: o.footer_sentence.rstrip('.'))
    link_url = Faker('uri')
    publish_after = Faker(
        'past_datetime',
        start_date='-30d',
        tzinfo=timezone.utc
    )
    expires = None
    order = 0

    title_sentence = Faker('sentence', nb_words=4)
    description_paragraphs = Faker('paragraphs', nb=2)
    link_label_words = Faker('words', nb=3)
    footer_sentence = Faker('sentence', nb_words=5)

    @post_generation
    def image_name(self, create, extracted, **kwargs):
        self.image.name = Faker('generic_image').generate({})
