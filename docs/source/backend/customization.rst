Customization Guide
===================

The tool's model card generation process leans heavily on a toolkit developed by Google. While the base toolkit is comprehensive, we've incorporated custom modifications to better align with project-specific needs. This includes additional native sections and an extended format to accommodate user-defined sections.

This guide outlines a procedure to integrate a new section into the model card. For our example, we'll incorporate an "Environmental Impact" section. 

Initial Setup
-------------

1. **Clone the Modified Library**: Start by cloning our modified library. Please note that you might need special permissions for this step.

    .. code-block:: bash

       git clone https://github.com/mcmi-group/featai_lib

Adding a New Section
--------------------

2. **Modify Essential Files**: Navigate to the ``model-card-toolkit`` folder. You'll need to update these files:

    - ``model_card.py``
    - ``core.py``
    - ``proto/model_card.proto``
    - ``template/test/default_template.html.jinja``

3. **Incorporate Environmental Impact in `model_card.py`**:

    Insert the following sections before the ``class ModelCard(BaseModelCardField):`` class definition:

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

    Now, inside the ``class ModelCard(BaseModelCardField):`` class definition, integrate the reference for the new section:

    .. code-block:: python

        enviromental_impact: EnvironmentalImpact = dataclasses.field(
        default_factory=EnvironmentalImpact)

4. **Update `core.py`**: At approximately line 326, append the following:

    .. code-block:: python

       environmental_impact = model_card.environmental_impact,

5. **Alter `proto/model_card.proto`**:

    Define your new data structures using the following code. Here we also see a similar structure as in `model_card.py`. First comes the child classes then parent classes:

    .. code-block:: proto

        message HardwareInformation {
          // Information for the used hardware in training
          optional string gpu_name = 1;
          optional string gpu_tdp = 2;
          optional string cpu_name = 3;
          optional string cpu_tdp = 4;
        }

        message TrainingEnvironment {
          // Information on training environment 
          optional string total_time = 1;
          optional string co2_kwh = 2;
        }

        message EnvironmentalImpact {
          // Environmental impact of the training process
          repeated HardwareInformation hardware_information = 1;
          repeated TrainingEnvironment training_enviroment = 2;
        }

    Then, within the parent model card class, add:

    .. code-block:: proto

       optional EnvironmentalImpact environmental_impact = 11;

6. **Enhance Rendering in `template/test/default_template.html.jinja` **:

    Incorporate the provided Jinja template snippet before the extended sections code:

    .. code-block:: jinja

       <div class="row">
       {% if environmental_impact and (environmental_impact.hardware_information or environmental_impact.training_environment) %}
         <div class="col card">
         <h2>Environmental Impact</h2>
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

    Finally, copy this updated template to the ``model_card_v2\template\html`` folder within the main repository.

Building & Installing the Modified Library
------------------------------------------

7. **Build the Library**:
   
   Use the following command to build the library:

    .. code-block:: bash
    
        chmod +x model_card_toolkit/move_generated_files.sh

        pip install wheel

        python3 setup.py sdist bdist_wheel


    .. note::

        Before compiling the library, consider installing `Bazel <https://bazel.build/install>`_. Bazel might present challenges on Windows, but utilizing WSL2 (Windows Subsystem for Linux 2) can alleviate most issues.

8. **Install the New Library**:

    - Move the ``model_card_toolkit-2.0.0.dev0-py3-none-any.whl`` file from the recently created dist folder to the ``utils`` directory in the main repository.

    - Install the library to your enviroment while within the ``utils`` directory. You might need to use `--force-reinstall` flag. 

    .. code-block:: bash

        pip install --upgrade model_card_toolkit-2.0.0.dev0-py3-none-any.whl

9.  **Modify the `model_card_lib_v2.py` in the `utils` Folder**:

    Append the provided Python code snippet before the ``mct.update_model_card(model_card)``:

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
 

For a comprehensive breakdown of user input incorporation and other specific functions, refer to the `Django Backend Framework <source/backend/django_backend.rst>`_.

Final Thoughts
--------------

Remember to commit and push your changes to the repository. Subsequently, you can update the website to reflect these changes. While customization of the core library is reserved for native section additions, template modifications might be more frequent.
