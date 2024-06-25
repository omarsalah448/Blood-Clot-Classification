using System.ComponentModel.DataAnnotations;

namespace Mayo_Clinic.Models
{
    public class Doctor
    {
        public string Id { get; set; }

        [DataType(DataType.Text, ErrorMessage = "Not A Valid University Name")]
        public string University { get; set; } = string.Empty;

        [DataType(DataType.MultilineText)]
        public string Description { get; set; } = string.Empty;

        [DataType(DataType.ImageUrl, ErrorMessage = "Not A Valid Image URL")]
        public string Image { get; set; } = string.Empty;
    }
}
