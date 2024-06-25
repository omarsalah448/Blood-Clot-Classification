using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace Mayo_Clinic.Models
{
    public class ProfilePatientViewModel
    {
        public int Id { get; set; }

        [Required]
        [DataType(DataType.Text, ErrorMessage = "Not A Valid Name")]
        public string Name { get; set; }

        [Display(Name = "Phone Number")]
        [DataType(DataType.PhoneNumber, ErrorMessage = "Not A Valid Phone Number")]
        public string PhoneNumber { get; set; } = string.Empty;

        public int Age { get; set; }

        [Required]
        [Display(Name = "Blood Clot Image")]
        [DataType(DataType.ImageUrl, ErrorMessage = "Not A Valid Image URL")]
        public string BloodClotImage { get; set; }

        [Required]
        [RegularExpression("^(Unknown|CE|LAA|Other)$", ErrorMessage = "Value must be 'CE' or 'LAA'")]
        public string Classification { get; set; }
    }
}
