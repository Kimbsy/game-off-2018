import pygame, os, random

# Import helper functions.
from helpers import *

# Import sprites.
from sprites.base_sprites import BaseSprite, ImageSprite, ButtonSprite, TextSprite

pygame.init()
pygame.mixer.init()

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
            "I'll take 8!",
            "Perfect! An unmitigated sucess.",
            "This has the potential to be genuinely game changing.",
        ],
        'min_score': 8,
        'max_score': 10,
    },
    'medium': {
        'templates': [
            "I mean, sure, why not?",
            "It's not the most elegant, but it gets the job done.",
            "I don't think anyone would need more than one.",
            "I don't hate it.",
            "Comparable in greatness to sliced bread, but certainly not better.",
        ],
        'min_score': 5,
        'max_score': 7,
    },
    'bad': {
        'templates': [
            "This is really not what I had in mind.",
            "It just doesn't work. I don't see it catching on.",
            "At least their refund policy is fair.",
            "I do not like this.",
            "meh",
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
            "This is just not smart",
            "There is no way that is even legal.",
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

    def __init__(self, x, y, w, h, company, product):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.done = False
        self.company = company
        self.product = product
        self.font = pygame.font.SysFont(None, 25)
        self.text_color = (0, 0, 0)

        # Call the parent constructor
        super(NewspaperSprite, self).__init__(x, y)

    def init_image(self):
        self.image = pygame.Surface((self.w, self.h))
        self.image.fill((150, 150, 150))

        name = self.product.get('name')

        # Display the article title.
        title = self.font.render(name, True, self.text_color)
        pos = ((self.w * 0.5) - (title.get_size()[0] * 0.5), (self.h * 0.075))
        self.image.blit(title, pos)

        # Generate a tagline.
        tagline_template = random.choice(tagline_templates)
        tagline_text = tagline_template.format(self.company, name)
        tagline_text_box = TextSprite(self.x,
                                      self.y,
                                      (self.w * 0.6),
                                      (self.h * 0.9),
                                      tagline_text)
        self.image.blit(
            tagline_text_box.image,
            ((self.w * 0.05), (self.h * 0.2))
        )

        # Display the product image.
        product_image = ImageSprite(0, 0, self.product.get('img'))
        scaled_image = aspect_scale(product_image.image, ((self.w * 0.5), (self.h * 0.5)))
        self.image.blit(scaled_image, ((self.w * 0.65) , (self.h * 0.2)))

        # Choose a type of review
        # TODO: in future, make this based on the quality of the product.
        review_type = random.choice(list(review_templates.keys()))
        if (random.random() < 0.05):
            review_type = 'very_bad'
        
        # Display the reviews with their scores.
        reviews = get_reviews(review_type)
        y_offset = self.h * 0.4
        for review in reviews:
            score = review.get('score')
            text = review.get('text') + '  ' + str(score) + '/10'
            review_text_box = TextSprite(
                self.x,
                self.y,
                (self.w * 0.5),
                (self.h * 0.5),
                text
            )
            self.image.blit(review_text_box.image, ((self.w * 0.075), y_offset))
            y_offset += 50

        self.original_image = self.image
        self.original_scale = (self.w, self.h)
        self.current_modifier = 0.004
        self.image = pygame.transform.scale(self.image, self.get_current_scale())

    def get_current_scale(self):
        return (
            int(self.original_scale[0] * self.current_modifier),
            int(self.original_scale[1] * self.current_modifier)
        )

    def get_current_angle(self):
        return 1080 * self.current_modifier

    def get_current_pos_offset(self):
        original_w, original_h = self.original_scale
        current_w, current_h = self.get_current_scale()
        
        x_offset = self.x + (original_w * 0.5) - (current_w * 0.5)
        y_offset = self.y + (original_h * 0.5) - (current_h * 0.5)

        return (x_offset, y_offset)

    def update(self):
        """Increment the current scale modifier, then set the image to a
        scaled version of the image.
        """
        if (self.current_modifier < 1.0):
            self.current_modifier += 0.004
            self.image = pygame.transform.rotozoom(
                self.original_image,
                self.get_current_angle(),
                self.current_modifier
            )
            offset = self.get_current_pos_offset()
            self.rect.x = offset[0]
            self.rect.y = offset[1]
        else:
            self.current_modifier = 1.0
            self.image = self.original_image
            self.done = True

class MoneySprite(BaseSprite):
    """This sprite count up the amount of money the player has made from
    selling their product.
    """

    def __init__(self, x, y, profit, channel):
        self.profit = profit
        self.current = 0.0
        self.done = False
        self.font = pygame.font.SysFont(None, 30)
        self.text_color = (25, 180, 20)
        self.channel = channel
        self.sound = pygame.mixer.Sound(os.getcwd() + '/data/sounds/get_coin.wav')

        # Call the parent constructor.
        super(MoneySprite, self).__init__(x, y)

    def init_image(self):
        current_string = "£{0:.2f}".format(self.current)
        self.image = self.font.render(current_string, True, self.text_color)

    def update(self):
        if (self.current < self.profit):
            self.current += 0.01
            self.init_image()
            self.channel.play(self.sound)
        else:
            self.done = True

def sell(product):
    return round(random.uniform(1.0, 15.0), 2) # TODO: make this depend on the product.

def result_loop(game_state):
    """The result screen loop.
    """

    # TEST DATA
    # game_state.update({'latest_product': {
    #     'name': 'Roto-Raker 4000',
    #     'img' : os.getcwd() + '/data/pixel-components/pixel-pot.png',
    #     'components': ['rake', 'lawnmower'],
    #     'total_cost': 10.45,
    # }})

    game_surface = game_state.get('game_surface')
    screen_size = game_state.get('screen_size')
    screen_width = screen_size[0]
    screen_height = screen_size[1]
    channel = game_state.get('mixer_channels')[0]
    product = game_state.get('latest_product')
    company = game_state.get('company_name')

    # Main group of sprites to display.
    all_sprites = pygame.sprite.OrderedUpdates()
    w = (screen_width * 0.6)
    h = (screen_height * 0.6)
    x = (screen_width - w) * 0.5
    y = (screen_height - h) * 0.4
    newspaper = NewspaperSprite(
        x,
        y,
        w,
        h,
        company,
        product
    )
    all_sprites.add(newspaper)

    # Money counter, gets added after newspaper is done.
    available_funds = game_state.get('available_funds')
    profit = sell(product)
    game_state.update({'available_funds': available_funds + profit})
    money = MoneySprite(
        (screen_width * 0.5),
        (screen_height * 0.85),
        profit,
        channel
    )
    no_money = True

    # Done button, gets added after money is counted.
    done_button = ButtonSprite(
        (screen_width * 0.05),
        (screen_height * 0.05),
        'Done!',
        switch_to_screen,
        ['workshop_screen']
    )
    no_button = True

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

        # Update.
        for sprite in all_sprites:
            sprite.update()


        if (no_money and newspaper.done):
            pygame.time.wait(400)
            all_sprites.add(money)
            no_money = False
        if (no_button and money.done):
            all_sprites.add(done_button)
            no_button = False

        # Display.
        game_surface.fill((0, 0, 0))
        all_sprites.draw(game_surface)
        pygame.display.update()

    return game_state
