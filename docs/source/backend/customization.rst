CUSTOMIZATION
=============

As mentioned in the main page of the tool, the model card generation based on a toolkit provided by Google.
In the current status, there have been some modification made to the tool to make it more suitable for the project.
These modifications are more native sections and some extended sections to allow users add their own sections.

Here step-by-step instructions to add new section to the model card that will be rendered in the website and final model card.

- Clone the modified library first (special permissions might be needed)
    .. code-block:: bash
   
      git clone https://github.com/mcmi-group/featai_lib

- In the ``model-card-toolkit`` folder we need to change the following files:

    - `model_card.py`
    - `core.py`
    - `proto/model_card.proto`
    - `template/test/default_template.html.jinja`


Let's say we want to add an Environmental Impact section to the model card. We will update the code and you can actually see in the Repository.



- To integrate an "Environmental Impact" section into the model card, you should modify the `model_card.py` file. Incorporate the following code snippets right before the ``class ModelCard(BaseModelCardField):`` class definiton. This structure ensures that the code remains organized and easy to maintain.

    .. code-block:: python

        @dataclasses.dataclass
        class HardwareInformation(BaseModelCardField):
            """
            Field is intended to capture the hardware information from the user.

            Attributes:
                gpu_name: Name of the GPU
                gpu_tdp: TDP of the GPU
                cpu_name: Name of the CPU
                cpu_tdp: TDP of the CPU
            """
            gpu_name: Optional[str] = None
            gpu_tdp: Optional[str] = None
            cpu_name: Optional[str] = None
            cpu_tdp: Optional[str] = None

            _proto_type: dataclasses.InitVar[Type[
                model_card_pb2.HardwareInformation]] = model_card_pb2.HardwareInformation

        @dataclasses.dataclass
        class TrainingEnvironment(BaseModelCardField):
            """
            Field is intended to capture the environment specifics during training.

            Attributes:
                total_time: Total time taken for training
                co2_kwh: CO2 emission in KWH for the respective country
            """
            total_time: Optional[str] = None
            co2_kwh: Optional[str] = None

            _proto_type: dataclasses.InitVar[Type[
                model_card_pb2.TrainingEnvironment]] = model_card_pb2.TrainingEnvironment

        @dataclasses.dataclass
        class EnvironmentalImpact(BaseModelCardField):
            """
            This section is designed to inform users about the environmental impact of the model.

            Attributes:
                hardware_information: List of hardware utilized
                training_environment: Details about the training environment
            """
            hardware_information: List[HardwareInformation] = dataclasses.field(default_factory=list)
            training_environment: List[TrainingEnvironment] = dataclasses.field(default_factory=list)

            _proto_type: dataclasses.InitVar[Type[
                model_card_pb2.EnvironmentalImpact]] = model_card_pb2.EnvironmentalImpact

- We should also add our new section in the parent model card class. Add the following code snippet to the ``class ModelCard(BaseModelCardField):`` class definition.

    .. code-block:: python

        enviromental_impact: EnvironmentalImpact = dataclasses.field(
        default_factory=EnvironmentalImpact)

- Next, we have to modify the `core.py` file. We add to the line 326 following:
  
    .. code-block:: python

        environmental_impact = model_card.environmental_impact,  

- We also need to modify the `proto/model_card.proto` file. Here we also see a similar structure as in `model_card.py`. First comes the child classes then parent classes.

    .. code-block:: proto

        message HardwareInformation {
          // Information for the used hardware in training
          // Next tag number is 5
          optional string gpu_name = 1;
          optional string gpu_tdp = 2;
          optional string cpu_name = 3;
          optional string cpu_tdp = 4;

        }

        message TrainingEnvironment {
          // Information on training environment 
          // Next tag number is 3
          optional string total_time = 1;
          optional string co2_kwh = 2;

        }

        message EnvironmentalImpact {
          // Environmental impact of the training process
          repeated HardwareInformation hardware_information = 1;
          repeated TrainingEnvironment training_enviroment = 2;
        }

- Then the parent model card class add line 1063 following:
    .. code-block:: proto

       optional EnvironmentalImpact environmental_impact = 11;

- Now we can already build the library but modifying the template the render these modifications would be a good idea. For that we go the the `template/test/default_template.html.jinja` and add the following before the extended sections code. Important point here there is no one correct way to render it in the template. What is below is just an example.
  
    .. code-block:: jinja

       <div class="row">
       {% if environmental_impact and (environmental_impact.hardware_information or environmental_impact.training_environment)%}
         <div class="col card">
         <h2>Enviromental Impact</h2>
           {% if environmental_impact.hardware_information %}
               <h3>Hardware Information</h3>
               <ul>
                   {% for info in environmental_impact.hardware_information %}
                       <li>
                           <div>GPU Name: {{ info.gpu_name }}</div>
                           <div>GPU TDP : {{ info.gpu_tdp }}</div>
                           <div>CPU Name: {{ info.cpu_name }}</div>
                           <div>CPU TDP: {{ info.cpu_tdp }}</div>
                       </li>
                   {% endfor %}
               </ul>
           {% endif %}
           {% if environmental_impact.TrainingEnvironment %}
               <h3>Training Information</h3>
               <ul>
                   {% for info in environmental_impact.TrainingEnvironment %}
                       <li>
                           <div>Runtime: {{ info.total_time }}</div>
                           <div>Co2/kWh: {{ info.co2_kwh }}</div>
                       </li>
                   {% endfor %}
               </ul>
         {% endif %}  
         </div>
       </div>      

- Now we can build the library
    
    .. code-block:: bash
    
        chmod +x model_card_toolkit/move_generated_files.sh

        pip install wheel

        python3 setup.py sdist bdist_wheel

- Copy the `model_card_toolkit-2.0.0.dev0-py3-none-any.whl` from the newly created dist folder to the `utils` folder

- Then, install it in the `utils` folder

    .. code-block:: bash

        pip install --upgrade model_card_toolkit-2.0.0.dev0-py3-none-any.whl

- Now we can use the new library to populate the new section in the model card. For that we need to modify the `model_card_lib_v2.py` file in the `utils` folder. We add the following code snippet to the `model_card_lib_v2.py` file right before the `mct.update_model_card(model_card)`.

    .. code-block:: python

        # Environmental Impact
        model_card.enviromental_impact.hardware_information = [mctlib.HardwareInformation(
            gpu_name="NVIDIA Tesla V100",
            gpu_tdp="250W",
            cpu_name="Intel(R) Xeon(R) CPU @ 2.30GHz",
            cpu_tdp="150W"
        )]
        model_card.enviromental_impact.training_environment = [mct.TrainingEnvironment(
            total_time="2h",
            co2_kwh="0.0005"
        )]
 

Above just a usage of the new section is shown. There are other functions to streamline the taken input from the user and incorporate it to the population of model card. For more information please refer to the `Django Backend Framework <backend/django_backend.rst>`_.


The next steps would be commiting the changes and pushing it to the repository. From there, the website can be updated.  

Customization of the core library only needed when a native section needed to be added. However, customization of the jinja template may be needed more frequent.
