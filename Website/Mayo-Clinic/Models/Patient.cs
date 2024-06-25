using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace Mayo_Clinic.Models
{
    public class Patient
    {
        public int Id { get; set; }

        [Required]
        [DataType(DataType.Text, ErrorMessage = "Not A Valid Name")]
        public required string Name { get; set; }

        [Display(Name = "Phone Number")]
        [DataType(DataType.PhoneNumber, ErrorMessage = "Not A Valid Phone Number")]
        public string PhoneNumber { get; set; } = string.Empty;

        [Display(Name = "Birth Date")]
        [DataType(DataType.Date, ErrorMessage = "Not A Valid Birth Date")]
        public DateOnly BirthDate { get; set; } = new DateOnly();

        [Required]
        [Display(Name = "Blood Clot Image")]
        [DataType(DataType.ImageUrl, ErrorMessage = "Not A Valid Image URL")]
        public required string BloodClotImage { get; set; }

        [Required]
        [RegularExpression("^(Unknown|CE|LAA|Other)$", ErrorMessage = "Value must be 'CE' or 'LAA'")]
        public required string Classification { get; set; }

        [ForeignKey("Doctor")]
        public string Docotor_Id { get; set; } = string.Empty;
        public virtual Doctor? Doctor { get; set; }
    }
}
