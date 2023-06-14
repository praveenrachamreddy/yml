import subprocess

# Function to create a Spring Boot RESTful API project
def create_spring_boot_rest_api():
    user_input = input("Enter the name of the project: ")
    project_name = user_input.capitalize().replace(" ", "")

    # Generate pom.xml content
    pom_xml_content = f"""
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.example</groupId>
  <artifactId>{project_name}</artifactId>
  <version>1.0-SNAPSHOT</version>

  <properties>
    <java.version>11</java.version>
    <spring-boot.version>2.5.0</spring-boot.version>
  </properties>

  <dependencies>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <!-- Add more dependencies as needed -->
  </dependencies>
</project>
    """

    # Create file tree and write code
    src_directory_structure = f"- src/main/java/com/example/{project_name}/\n  - {project_name}Application.java\n  - controller/\n    - HelloController.java"
    resources_directory_structure = f"- src/main/resources/\n  - application.properties"
    create_file_tree(src_directory_structure)
    create_file_tree(resources_directory_structure)

    # Write code to files
    write_code_to_file(f"src/main/java/com/example/{project_name}/{project_name}Application.java", generate_spring_boot_application_code(project_name))
    write_code_to_file(f"src/main/java/com/example/{project_name}/controller/HelloController.java", generate_hello_controller_code())
    write_code_to_file("src/main/resources/application.properties", generate_application_properties_code())

    # Write pom.xml file
    write_code_to_file("pom.xml", pom_xml_content)

    # Provide feedback to the user
    feedback = f"Spring Boot RESTful API project '{project_name}' created successfully!\n"
    feedback += "The project structure and files have been created with the following contents:\n\n"
    feedback += "src/main/java/com/example/{project_name}/{project_name}Application.java:\n\n"
    feedback += generate_spring_boot_application_code(project_name) + "\n\n"
    feedback += "src/main/java/com/example/{project_name}/controller/HelloController.java:\n\n"
    feedback += generate_hello_controller_code() + "\n\n"
    feedback += "src/main/resources/application.properties:\n\n"
    feedback += generate_application_properties_code() + "\n\n"
    feedback += "pom.xml:\n\n"
    feedback += pom_xml_content

    print(feedback)

    # Run Maven commands to build and run the project
    subprocess.run(["mvn", "clean", "install"], cwd=project_name, shell=True)
    subprocess.run(["mvn", "spring-boot:run"], cwd=project_name, shell=True)


# Function to generate Spring Boot Application code
def generate_spring_boot_application_code(project_name):
    return f"""
package com.example.{project_name};

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class {project_name}Application {{
    public static void main(String[] args) {{
        SpringApplication.run({project_name}Application.class, args);
    }}
}}
"""


# Function to generate HelloController code
def generate_hello_controller_code():
    return """
package com.example.{project_name}.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
public class HelloController {

    @GetMapping("/hello")
    public String sayHello() {
        return "Hello, World!";
    }
}
"""


# Function to generate application.properties code
def generate_application_properties_code():
    return """
# Server port
server.port=8080

# Application name
spring.application.name={project_name}
"""


# Rest of the code...

# Main program loop
while True:
    user_input = input("Enter your request (or 'exit' to quit): ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    # Handle user requests
    if any(keyword in user_input.lower() for keyword in ["spring boot restful api"]):
        create_spring_boot_rest_api()
    else:
        print(f"Sorry, I can only handle requests related to creating a {user_input.capitalize()} project.")
