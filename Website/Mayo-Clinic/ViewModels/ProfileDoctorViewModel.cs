using System.ComponentModel.DataAnnotations;

namespace Mayo_Clinic.ViewModels
{
    public class ProfileDoctorViewModel
    {
        [Required]
        [Display(Name = "First Name:")]
        [DataType(DataType.Text)]
        public required string FirstName { get; set; } = string.Empty;

        [Display(Name = "Last Name:")]
        [DataType(DataType.Text)]
        public string LastName { get; set; } = string.Empty;

        [Required]
        [Display(Name = "User Name:")]
        public string UserName { get; set; } = string.Empty;

        [DataType(DataType.Text, ErrorMessage = "Not A Valid University Name")]
        public string University { get; set; } = string.Empty;

        [DataType(DataType.MultilineText)]
        public string Description { get; set; } = string.Empty;

        [Display(Name = "Image URL:")]
        [DataType(DataType.ImageUrl, ErrorMessage = "Not A Valid Image URL")]
        public string Image { get; set; } = string.Empty;
    }
}
