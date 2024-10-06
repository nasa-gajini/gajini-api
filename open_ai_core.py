import os
import base64
import requests
from dotenv import load_dotenv
from PIL import Image

# Load environment variables from .env file
load_dotenv()

# Function to convert Evap_tavg (kg/m²/s) to mm/day
def evap_kgm2s_to_mmd(evap_value_kg_m2_s):
    # 1 kg m^-2 s^-1 = 86400 mm/day
    return evap_value_kg_m2_s * 86400
# Get OpenAI API key from .env
openai_api_key = os.getenv("OPENAI_API_KEY")

# Function to query OpenAI API for the extracted data
def query_openai(prompt, crop, evap_value, soil_moisture, vegetation_water_content, vegetation_opacity, bulk_density, clay_fraction, surface_temperature, static_water_body_fraction, ndvi, lon, lat):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }

    # Create a question for the AI including all variables
    user_question = (
        f"{prompt} The environmental data for latitude {lat} and longitude {lon} in Egypt is as follows:\n"
        f"- Evapotranspiration (ET): {evap_value} mm/day\n"
        f"- Soil Moisture: {soil_moisture} m³/m³\n"
        f"- Vegetation Water Content: {vegetation_water_content} kg/m²\n"
        f"- Vegetation Opacity: {vegetation_opacity}\n"
        f"- Bulk Density: {bulk_density} g/cm³\n"
        f"- Clay Fraction: {clay_fraction}\n"
        f"- Surface Temperature: {surface_temperature} K\n"
        f"- Static Water Body Fraction: {static_water_body_fraction}\n"
        f"- NDVI: {ndvi}\n\n"
        f"The farmer is currently growing {crop}. Based on the current environmental conditions and the specific needs of {crop}, please provide the following:\n"
        f"1) A diagnosis of the current state of the field for {crop} based on the environmental data provided.\n"
        f"2) An optimized irrigation plan tailored for {crop} to improve water usage and crop yield. Please also explain the reasoning behind this plan and how it will benefit the crop in the given environmental conditions."
    )

    payload = {
        "model": "gpt-4",
        "messages": [
            {
                "role": "user",
                "content": user_question
            }
        ],
        "max_tokens": 800
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    # Handle response and check for errors
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}, {response.text}"

# Main function
def main():
    # Define file path and the coordinates (lon, lat) you want to query
    file_path = '../data/Vegetation_ET/FLDAS_NOAH01_C_GL_M.A202408.001.nc'
    lon = 31.233  # 카이로의 경도
    lat = 30.033  # 카이로의 위도

    # SMAP 데이터 값 (테스트용 샘플 값 사용)
    evap_value = 4.5  # mm/day
    soil_moisture = 0.2  # m³/m³
    vegetation_water_content = 0.15  # kg/m²
    vegetation_opacity = 0.8
    bulk_density = 1.3  # g/cm³
    clay_fraction = 0.25
    surface_temperature = 300  # K (Kelvin)
    static_water_body_fraction = 0.1

    # NVDI
    ndvi = 0.65

    # ET
    evap_value_kg_m2_s = 1.5e-5  # kg/m²/s 단위의 샘플 값
    evap_value = evap_kgm2s_to_mmd(evap_value_kg_m2_s)  # mm/day로 변환

    # Define a prompt to ask OpenAI
    prompt = (
        "This dataset contains environmental factors such as evapotranspiration, soil moisture, "
        "and other critical information for understanding agriculture and water resource management. "
        "Given these current environmental conditions, please recommend which crops would be suitable for cultivation in the Cairo region of Egypt."
    )

    # Get description from OpenAI based on the extracted value
    response = query_openai(prompt, evap_value, soil_moisture, vegetation_water_content, vegetation_opacity,
                            bulk_density, clay_fraction, surface_temperature, static_water_body_fraction, ndvi, lon,
                            lat)

    # Print the response from OpenAI
    print("AI Response:", response)


if __name__ == "__main__":
    main()