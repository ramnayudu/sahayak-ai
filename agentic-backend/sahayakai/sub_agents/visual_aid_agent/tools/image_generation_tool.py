from datetime import datetime
import os
from google import genai
from google.genai import types
from google.adk.tools import ToolContext
from google.cloud import storage
from .... import config


# Only initialize the cloud client if not using local model
if not config.USE_LOCAL_MODEL:
    # Initialize the client with proper project configuration
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT') or config.GOOGLE_CLOUD_PROJECT
    location = os.getenv('GOOGLE_CLOUD_LOCATION') or config.GOOGLE_CLOUD_LOCATION

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")

    client = genai.Client(
        vertexai=True,
        project=project_id,
        location=location
    )
else:
    client = None


async def generate_images(imagen_prompt: str, tool_context: ToolContext):
    """Generate images using either cloud or local model approach"""
    
    # If using local model, provide a text-based response instead of actual image generation
    if config.USE_LOCAL_MODEL:
        return await generate_local_visual_aid(imagen_prompt, tool_context)
    
    # Original cloud-based image generation
    try:
        response = client.models.generate_images(
            model="imagen-3.0-generate-002",
            prompt=imagen_prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="9:16",
                safety_filter_level="block_low_and_above",
                person_generation="allow_adult",
            ),
        )
        generated_image_paths = []
        if response.generated_images is not None:
            for generated_image in response.generated_images:
                # Get the image bytes
                image_bytes = generated_image.image.image_bytes
                counter = str(tool_context.state.get("loop_iteration", 0))
                artifact_name = f"generated_image_" + counter + ".png"
                # call save to gcs function
                #if config.GCS_BUCKET_NAME:
                    #save_to_gcs(tool_context, image_bytes, artifact_name, counter)

                # Save as ADK artifact (optional, if still needed by other ADK components)
                report_artifact = types.Part.from_bytes(
                    data=image_bytes, mime_type="image/png"
                )

                await tool_context.save_artifact(artifact_name, report_artifact)
                print(f"Image also saved as ADK artifact: {artifact_name}")

                return {
                    "status": "success",
                    "message": f"Image generated .  ADK artifact: {artifact_name}.",
                    "artifact_name": artifact_name,
                }
        else:
            # model_dump_json might not exist or be the best way to get error details
            error_details = str(response)  # Or a more specific error field if available
            print(f"No images generated. Response: {error_details}")
            return {
                "status": "error",
                "message": f"No images generated. Response: {error_details}",
            }

    except Exception as e:
        return {"status": "error", "message": f"No images generated. {e}"}


async def generate_local_visual_aid(imagen_prompt: str, tool_context: ToolContext):
    """Generate visual aid description for local model usage (text-based)"""
    try:
        # For local models, we'll provide detailed drawing instructions instead of actual images
        counter = str(tool_context.state.get("loop_iteration", 0))
        artifact_name = f"visual_aid_instructions_" + counter + ".txt"
        
        # Create detailed drawing instructions based on the prompt
        visual_instructions = f"""
🎨 VISUAL AID DRAWING INSTRUCTIONS
Topic: {imagen_prompt}

📋 Drawing Guide for Teachers:
1. MAIN ELEMENTS TO DRAW:
   - Central concept illustration
   - Supporting diagrams and labels
   - Step-by-step visual process (if applicable)

2. SUGGESTED LAYOUT:
   - Title at the top in large, clear letters
   - Main diagram in the center
   - Labels and annotations around key elements
   - Legend or key at the bottom (if needed)

3. DRAWING TIPS:
   - Use simple shapes (circles, rectangles, arrows)
   - Keep text large and readable from the back of the classroom
   - Use different colors if available (chalk, markers)
   - Make it interactive - leave space for student input

4. CULTURAL CONTEXT:
   - Include examples familiar to rural Indian students
   - Use locally relevant objects and scenarios
   - Consider multi-grade classroom needs

5. MATERIALS NEEDED:
   - Blackboard/whiteboard
   - Chalk/markers
   - Ruler (for straight lines)
   - Compass (for circles, if available)

📝 STEP-BY-STEP DRAWING PROCESS:
1. Start with the main frame/border
2. Add title and main heading
3. Draw central concept
4. Add supporting elements
5. Include labels and text
6. Add arrows and connections
7. Review and enhance clarity

💡 ENGAGEMENT IDEAS:
- Ask students to help with labeling
- Use the diagram for interactive questioning
- Allow students to add their own examples
- Create variations for different grade levels

This visual aid has been optimized for offline classroom use in rural Indian schools.
"""
        
        # Save as text artifact
        text_artifact = types.Part.from_text(visual_instructions)
        await tool_context.save_artifact(artifact_name, text_artifact)
        
        print(f"Visual aid instructions saved as: {artifact_name}")
        
        return {
            "status": "success",
            "message": f"Visual aid drawing instructions generated for local classroom use. Instructions saved as: {artifact_name}",
            "artifact_name": artifact_name,
            "instructions": visual_instructions
        }
        
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Failed to generate visual aid instructions: {str(e)}"
        }

    try:

        response = client.models.generate_images(
            model="imagen-3.0-generate-002",
            prompt=imagen_prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="9:16",
                safety_filter_level="block_low_and_above",
                person_generation="allow_adult",
            ),
        )
        generated_image_paths = []
        if response.generated_images is not None:
            for generated_image in response.generated_images:
                # Get the image bytes
                image_bytes = generated_image.image.image_bytes
                counter = str(tool_context.state.get("loop_iteration", 0))
                artifact_name = f"generated_image_" + counter + ".png"
                # call save to gcs function
                #if config.GCS_BUCKET_NAME:
                    #save_to_gcs(tool_context, image_bytes, artifact_name, counter)

                # Save as ADK artifact (optional, if still needed by other ADK components)
                report_artifact = types.Part.from_bytes(
                    data=image_bytes, mime_type="image/png"
                )

                await tool_context.save_artifact(artifact_name, report_artifact)
                print(f"Image also saved as ADK artifact: {artifact_name}")

                return {
                    "status": "success",
                    "message": f"Image generated .  ADK artifact: {artifact_name}.",
                    "artifact_name": artifact_name,
                }
        else:
            # model_dump_json might not exist or be the best way to get error details
            error_details = str(response)  # Or a more specific error field if available
            print(f"No images generated. Response: {error_details}")
            return {
                "status": "error",
                "message": f"No images generated. Response: {error_details}",
            }

    except Exception as e:

        return {"status": "error", "message": f"No images generated. {e}"}


def save_to_gcs(tool_context: ToolContext, image_bytes, filename: str, counter: str):
    # --- Save to GCS ---
    storage_client = storage.Client()  # Initialize GCS client
    bucket_name = config.GCS_BUCKET_NAME

    unique_id = tool_context.state.get("unique_id", "")
    current_date_str = datetime.utcnow().strftime("%Y-%m-%d")
    unique_filename = filename
    gcs_blob_name = f"{current_date_str}/{unique_id}/{unique_filename}"

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(gcs_blob_name)

    try:
        blob.upload_from_string(image_bytes, content_type="image/png")
        gcs_uri = f"gs://{bucket_name}/{gcs_blob_name}"

        # Store GCS URI in session context
        # Store GCS URI in session context
        tool_context.state["generated_image_gcs_uri_" + counter] = gcs_uri

    except Exception as e_gcs:

        # Decide if this is a fatal error for the tool
        return {
            "status": "error",
            "message": f"Image generated but failed to upload to GCS: {e_gcs}",
        }
        # --- End Save to GCS ---