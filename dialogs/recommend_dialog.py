# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from datatypes_date_time.timex import Timex

from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import ConfirmPrompt, TextPrompt, PromptOptions
from botbuilder.core import MessageFactory, TurnContext
from botbuilder.schema import InputHints, Attachment
from .cancel_and_help_dialog import CancelAndHelpDialog
from helpers._age_helper import age_cal
from helpers._function_helper import function_cal
from helpers._sex_helper import sex_cal
from helpers._style_helper import style_cal
from helpers._season_helper import season_cal
from helpers._color_helper import color_cal
from helpers._typ_helper import typ_cal
from helpers.cost_helper import cost_cal
from helpers.ok_helper import is_ok


from recommend.recommend import recommend

import json
import os.path
import time

import os
class RecommendDialog(CancelAndHelpDialog):
    def __init__(self, dialog_id: str = None):
        super(RecommendDialog, self).__init__(dialog_id or RecommendDialog.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.sex_step,
                    self.age_step,
                    self.season_step,
                    self.typ_step,
                    self.function_step,
                    self.style_step,
                    self.color_step,
                    self.cost_step,
                    self.confirm_step,
                    self.final_step,
                ],
            )
        )

        self.initial_dialog_id = WaterfallDialog.__name__

    async def sex_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        product_details = step_context.options

        if product_details.sex is None:
            message_text = "您的性别是？"
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        return await step_context.next(product_details.sex)

    async def age_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        product_details = step_context.options

        # Capture the response to the previous step's prompt
        product_details.sex = sex_cal(step_context.result)

        if product_details.age is None:
            message_text = "您是哪一年龄段人群（请在青少年、青年、中年、老年中选择一项回答）？"
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        return await step_context.next(product_details.age)


    async def season_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        product_details = step_context.options

        # Capture the response to the previous step's prompt
        product_details.age = age_cal(step_context.result)
        #print(product_details.age)
        if product_details.season is None:
            message_text = "这件衣服是在什么季节穿呢？"
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        return await step_context.next(product_details.season)

    async def typ_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        product_details = step_context.options

        # Capture the response to the previous step's prompt
        product_details.season = season_cal(step_context.result)

        if product_details.typ is None:
            if product_details.sex['sex-female'] == 10:
                message_text = "这件衣服属于什么类型呢（上衣或连衣裙）？"
            else:
                message_text = "这件衣服属于什么类型呢（上衣或T恤）？"
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        return await step_context.next(product_details.typ)



    async def function_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        product_details = step_context.options

        # Capture the response to the previous step's prompt
        product_details.typ = typ_cal(step_context.result)

        if product_details.function is None:
            message_text = "穿这件衣服的功能是什么呢（可从日常、运动、职场中选择回答）？"
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        return await step_context.next(product_details.function)
    async def style_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        product_details = step_context.options

        # Capture the response to the previous step's prompt
        product_details.function = function_cal(step_context.result)

        if product_details.style is None:
            message_text = "希望这件衣服是什么风格呢？"
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        return await step_context.next(product_details.style)
    async def color_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        product_details = step_context.options
        # Capture the response to the previous step's prompt
        product_details.style = style_cal(step_context.result)

        if product_details.color is None:
            message_text = "您希望这件衣服浅色还是深色？"
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        return await step_context.next(product_details.color)

    async def cost_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        product_details = step_context.options

        # Capture the response to the previous step's prompt
        product_details.color = color_cal(step_context.result)
        if product_details.color:
            with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/save/color.txt','a+') as f:
                f.write('light')
        else:
            with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/save/color.txt','a+') as f:
                f.write('deep')
        if product_details.cost is None:
            message_text = "您预期这件衣服是多少元呢（请以xxx-xxx的形式回答）？"
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        return await step_context.next(product_details.cost)



    async def confirm_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """
        Confirm the information the user has provided.
        :param step_context:
        :return DialogTurnResult:
        """
        product_details = step_context.options

        # Capture the results of the previous step
        product_details.cost = cost_cal(step_context.result)

        message_text = (
            #f"请确认：您购买电脑是为了 { product_details.use } 用途。"
            #f"您的预算为：{ product_details.cost['low'] }-{ product_details.cost['high'] }。"
            #f"您的外观需求为：{ product_details.looking}。"
            f"紧张计算中……"
        )
        time.sleep(1)
        calculating_message = MessageFactory.text(
            message_text, message_text, InputHints.ignoring_input
        )
        await step_context.context.send_activity(calculating_message)

        return await step_context.next(product_details.style)


    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """
        Complete the interaction and end the dialog.
        :param step_context:
        :return DialogTurnResult:
        """
        if step_context.result:
            product_details = step_context.options
            print(product_details.sex,product_details.age,product_details.season,
                product_details.typ,product_details.function,product_details.style,product_details.cost)
            recommend_id, recommend_result = recommend(product_details.sex,product_details.age,product_details.season,
                product_details.typ,product_details.function,product_details.style,product_details.cost)

            welcome_card = self.create_adaptive_card_attachment(recommend_id)
            response = MessageFactory.attachment(welcome_card)
            await step_context.context.send_activity(response)

            message_text = str(recommend_result)
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.ignoring_input
            )    
            await step_context.context.send_activity(prompt_message)
            '''
            pro_dict = {}
            pro_dict['sex'] = product_details.sex
            pro_dict['age'] = product_details.age
            pro_dict['season'] = product_details.season
            pro_dict['function'] = product_details.function
            pro_dict['style'] = product_details.style
            pro_dict['cost'] = product_details.cost
            '''
            with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/save/log.txt','a+') as f:
                f.write(str(recommend_id))
                f.write('\n')
            with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/save/pricelog.txt','w+') as f:
                f.write(str(product_details.cost))

            return await step_context.end_dialog(product_details)
        return await step_context.end_dialog()


    # Load attachment from file.
    def create_adaptive_card_attachment(self,id):
        relative_path = os.path.abspath(os.path.dirname(__file__))
        with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/save/color.txt','r+') as f:
            color = f.readline()
        if color =='deep':
            suffix = '.2'
            print('深色')
        else:
            suffix = '.1'
            print('浅色')
        path = os.path.join(relative_path, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/json/test.json")
        img_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/sources/img/'+str(id+1)+suffix+'.jpg'

        with open(path) as in_file:
            card = json.load(in_file)
            card['body'][0]['url'] = img_path
        with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/sources/test.txt','w+') as f:
            f.write(str(card))
        #print(card)
        return Attachment(
            content_type="application/vnd.microsoft.card.adaptive", content=card
        )
