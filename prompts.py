from langchain import PromptTemplate


class ArticlePromptCreator:
    def __init__(self, article: str):
        self.article = article
        self.template = """
-----------------INSTRUCTIONS START -----------------------
Assume you are a world class journalist that is carrying out research about the new Pixel 7a launch. 
You are very organized and want to highlight and tag articles to later process them further.

Read the article (from ARTICLE START to ARTICLE END) and extract quotes with their respective tags. 
If there is no information that can be added to a tag, do not return that tag. Only use the following tags: 

Features-Camera: Statements mentioning the Pixel 7a camera or photographic capabilities.
Features-Battery: Statements mentioning the Pixel 7a battery or battery capabilities (including charging).
Features-Build-Quality: Statements mentioning the Pixel 7a build quality (including how premium or not it feels).
Features-Gaming: Statements mentoning the Pixel 7a gaming capabilities. 
Features-Screen: Statements mentoning the screen quality, bezels, brightness, colour range. 
Pricing: Statements mentoning whether the Pixel 7a is well priced or not. 
Competitiveness: Statements comparing the Pixel 7a to Samsung Galaxy, Apple iPhone, or other Chinese OEMS like Oppo, Xiaomi, Reno. 
Company Strategy: Information regarding Google's strategy and what role this phone plays within that strategy.
Industry Analysis: Insights that provide a broader strategic context about the smartphone market.
Future Predictions: Predictions about the future of the Pixel series or Google's direction in the smartphone market.

Return your response as a JSON with the following format:

'[ 
  "Insider information": ["Quote a", "Quote B", "Quote C"], 
  "Company strategy": ["Quote A"]
]'

Everything between the ' ' must be valid json.

You can only tag a quote under one tag (do not repeatedly include the same quote in each tag). 

-----------------INSTRUCTIONS END -----------------------


-----------------ARTICLE START -----------------------

{article}

-----------------ARTICLE END -----------------------

RESPONSE: 


"""
        self.prompt = PromptTemplate(
                    input_variables=["article"],
                    template=self.template,
                )
    def create_prompt(self):
            return self.prompt.format(article=self.article)


# Usage:
prompt_creator = ArticlePromptCreator("this is an article")
print(prompt_creator.create_prompt())

