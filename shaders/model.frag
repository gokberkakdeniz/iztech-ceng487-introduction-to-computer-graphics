#version 330

in vec3 fragPos;
in vec4 fragColor;
in vec2 fragUV;
in vec4 fragNormal;

out vec4 outColor;

uniform float texBlendRatio;
uniform sampler2D tex1;
uniform sampler2D tex2;

uniform vec3 pointLight1Pos;
uniform vec4 pointLight1Color;
uniform float pointLight1Intensity;

uniform vec3 dirLight1Dir;
uniform vec4 dirLight1Color;
uniform float dirLight1Intensity;

uniform vec3 spotLight1Pos;
uniform vec3 spotLight1Dir;
uniform vec4 spotLight1Color;
uniform float spotLight1Angle;
uniform float spotLight1Intensity;

uniform vec3 cameraPos;
uniform bool blinEnabled;

void main()
{
    vec4 texVal1 = texture(tex1, fragUV);
    texVal1.a = texBlendRatio;
    
    vec4 texVal2 = texture(tex2, fragUV);
    texVal2.a = 1.0 - texBlendRatio;
    
    vec4 texBlendVal = mix(texVal1, texVal2, texVal2.a);

	vec4 pointLight1Dir = vec4(normalize(pointLight1Pos - fragPos), 1.0);
	float pointLight1nDotL = max(dot(fragNormal, pointLight1Dir), 0.0);
    vec4 pointLight1 = pointLight1Color * pointLight1Intensity * pointLight1nDotL;

	float dirLight1nDotL = max(dot(fragNormal, normalize(vec4(dirLight1Dir, 0.0))), 0.0);
    vec4 dirLight1 = dirLight1Color * dirLight1Intensity * dirLight1nDotL;

    float spotLight1Factor = 0.0;
    float spotLight1Cosine = dot(
        normalize(-spotLight1Dir),
        normalize(spotLight1Pos - fragPos)
    );
    if (spotLight1Cosine >= spotLight1Angle) { 
        spotLight1Factor = pow(spotLight1Cosine, 48);
    }
    vec4 spotLight1 = spotLight1Color * spotLight1Intensity * spotLight1Factor;

    float pointLight1Spec = 1.0;
    float dirLight1Spec = 1.0;

    if (blinEnabled) {
        vec4 viewDir = vec4(normalize(cameraPos - fragPos), 0.0);

        vec4 pointLight1halfwayDir = normalize(pointLight1Dir + viewDir);  
        pointLight1Spec = pow(max(dot(fragNormal, pointLight1halfwayDir), 0.0), 0.5);

        vec4 dirLight1halfwayDir = normalize(vec4(dirLight1Dir, 0.0) + viewDir);  
        dirLight1Spec = pow(max(dot(fragNormal, dirLight1halfwayDir), 0.0), 0.5);
    }

    vec4 lightVal = dirLight1 * dirLight1Spec + pointLight1 * pointLight1Spec + spotLight1;

    outColor = fragColor * texBlendVal * lightVal;
}