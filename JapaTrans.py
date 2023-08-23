from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import openai
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown

# OpenAI API key
openai.api_key = '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'

class ProofreaderApp(App):
    def build(self):
        self.chat_log = []

        layout = BoxLayout(orientation='vertical')

        # Create a dropdown for persona selection
        self.persona_dropdown = DropDown()
        for persona in ["Stewie", "GTA-V Trevor", "Quagmire", "Deadpool"]:
            btn = Button(
                text=persona, 
                size_hint_y=None, 
                height=45,
                background_color=("#617246")
            )
            btn.bind(on_release=lambda btn: self.persona_dropdown.select(btn.text))
            self.persona_dropdown.add_widget(btn)

        self.persona_button = Button(text='Select a Character', background_color=("#617246"), size_hint=(1, None), height=45)
        self.persona_button.bind(on_release=self.persona_dropdown.open)
        self.persona_dropdown.bind(on_select=lambda instance, x: setattr(self.persona_button, 'text', x))
        layout.add_widget(self.persona_button)

        self.text_widget = TextInput(
            multiline=True,
            font_size=30,
            halign='center',
            background_color=("#404a42"),
            foreground_color=("#f4f4f4")
        )
        layout.add_widget(self.text_widget)

        send_button = Button(
            text="Submit",
            background_color=("#192231"),
            font_size=35
        )
        send_button.bind(on_press=self.translator)
        layout.add_widget(send_button)

        self.output_label = TextInput(
            text="",
            font_size=30,
            halign='center',
            background_color=("#02000d"),
            foreground_color=("#f4f4f4")
        )
        layout.add_widget(self.output_label)

        return layout

    def translator(self, instance):
        persona = self.persona_button.text
        user_message = f"Reply as {persona}; " + self.text_widget.text.strip()
        self.chat_log.append({"role": "user", "content": user_message})
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=self.chat_log,
            temperature=0.1
        )

        assistant_response = response['choices'][0]['message']['content']
        self.chat_log.append({"role": "assistant", "content": assistant_response})

        self.display_summary(assistant_response)

    def display_summary(self, output):
        self.output_label.text = output

if __name__ == '__main__':
    app = ProofreaderApp()
    app.title = "Impostor"
    app.run()
