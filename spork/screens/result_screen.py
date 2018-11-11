import pygame
import random

# Import helper functions.
from helpers import *

# Import sprites.
from sprites.base_sprites import BaseSprite, ImageSprite, ButtonSprite, TextSprite

pygame.init()

tagline_templates = [
    "This week {0} released it's latest product: the {1}.",

    "New from {0}: the {1}!",

    "Get your hands on the new {1}, now available from {0}.",

    "People in your local area are going crazy for {0}'s {1}.",
]

review_templates = {
    'good': {
        'templates': [
            "I love it! This is exactly what I was looking for!",
            "Another smash hit! Will they ever stop nailing it?",
            "Why did we ever, ever, ever doubt? Truly inspiring.",
        ],
        'min_score': 8,
        'max_score': 10,
    },
    'medium': {
        'templates': [
            "I mean, sure, why not?",
            "It's not the most elegant, but it gets the job done.",
            "I don't think anyone would need more than one.",
        ],
        'min_score': 5,
        'max_score': 7,
    },
    'bad': {
        'templates': [
            "This is really not what I had in mind.",
            "It just doesn't work. I don't see it catching on.",
            "At least their refund policy is fair.",
        ],
        'min_score': 2,
        'max_score': 4,
    },
    'very_bad': {
        'templates': [
            "... Srsly?",
            "No.",
            "I can't even with this right now.",
            "I'm not reviewing that.",
        ],
        'min_score': 0,
        'max_score': 1,
    },
}

def get_reviews(review_type):

    template_options = review_templates.get(review_type).get('templates')
    min_score = review_templates.get(review_type).get('min_score')
    max_score = review_templates.get(review_type).get('max_score')

    templates = random.sample(template_options, 3)

    reviews = []

    for i in range(0, 3):
        reviews.append({
            'text': templates[i],
            'score': random.randint(min_score, max_score)
        })
    
    return reviews

class NewspaperSprite(BaseSprite):
    """This sprite contains the reviews of the product.
    """

    def __init__(self, x, y, company, product):
        self.company = company
        self.product = product
        self.font = pygame.font.SysFont(None, 25)
        self.text_color = (0, 0, 0)

        # Call the parent constructor
        super(NewspaperSprite, self).__init__(x, y)

    def init_image(self):
        self.image = pygame.Surface((800, 500))
        self.image.fill((150, 150, 150))

        name = self.product.get('name')

        # Display the article title.
        title = self.font.render(name, True, self.text_color)
        self.image.blit(title, (300, 20))

        # Generate a tagline.
        tagline_template = random.choice(tagline_templates)
        tagline_text = tagline_template.format(self.company, name)
        tagline_text_box = TextSprite(self.x, self.y, 400, 300, tagline_text)
        self.image.blit(tagline_text_box.image, (50, 75))

        # Display the product image.
        product_image = ImageSprite(0, 0, self.product.get('img'))
        scaled_image = aspect_scale(product_image.image, (250, 250))
        self.image.blit(scaled_image, (500, 50))

        # Choose a type of review
        # TODO: in future, make this based on the quality of the product.
        review_type = random.choice(list(review_templates.keys()))
        if (random.random() < 0.05):
            review_type = 'very_bad'
        
        # Display the reviews with their scores.
        reviews = get_reviews(review_type)
        y_offset = 200
        for review in reviews:
            score = review.get('score')
            text = review.get('text') + '  ' + str(score) + '/10'
            review_text_box = TextSprite(self.x, self.y, 400, 300, text)
            self.image.blit(review_text_box.image, (50, y_offset))
            y_offset += 50

def result_loop(game_state):
    """The result screen loop.
    """

    # TODO: This is temporary, should be stored in game_state by splicer on submission.
    game_state.update({'latest_product': {
        'name': 'Roto-Raker 4000',
        'img' : 'pixel-components/pixel-pot.png',
        'components': ['rake', 'lawnmower'],
        'total_cost': 10.45,
    }})

    # Main group of sprites to display.
    all_sprites = pygame.sprite.Group()
    all_sprites.add(
        NewspaperSprite(300, 150, game_state.get('company_name'), game_state.get('latest_product')),
        ButtonSprite(50, 50, 'Awesome!', switch_to_screen, ['workshop_screen']),
    )

    game_surface = game_state.get('game_surface')

    # Want to refactor this body into seperate functions.
    while not game_state.get('screen_done'):

        # Handle events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game(game_state)

            elif event.type == pygame.MOUSEBUTTONDOWN:                
                b = button_at_point(all_sprites, event.pos)
                if b:
                    game_state = b.on_click(game_state)

        # Display.
        game_surface.fill((0, 0, 0))
        all_sprites.draw(game_surface)
        pygame.display.update()

    return game_state
