using System.ComponentModel.DataAnnotations;

namespace Mayo_Clinic.ViewModels
{
    public class RegisterDoctorViewModel
    {
        [Required]
        [Display(Name = "First Name:")]
        [DataType(DataType.Text)]
        public required string FirstName { get; set; } = string.Empty;

        [Display(Name = "Last Name:")]
        [DataType(DataType.Text)]
        public string LastName { get; set; } = string.Empty;

        [Display(Name = "Birth Date:")]
        [DataType(DataType.Date, ErrorMessage = "Not A Valid Birth Date")]
        public DateOnly BirthDate { get; set; } = new DateOnly();

        [Display(Name = "Phone Number:")]
        [DataType(DataType.PhoneNumber, ErrorMessage = "Not A Valid Phone Number")]
        public required string PhoneNumber { get; set; } = string.Empty;

        [Required]
        [Display(Name = "Email:")]
        [DataType(DataType.EmailAddress, ErrorMessage = "Not A Valid Email")]
        public string Email { get; set; } = string.Empty;

        [Required]
        [Display(Name = "User Name:")]
        public string UserName { get; set; } = string.Empty;

        [Required]
        [Display(Name = "Password:")]
        [DataType(DataType.Password)]
        public string Password { get; set; } = string.Empty;

        [Required]
        [DataType(DataType.Password)]
        [Display(Name = "Confirm Password:")]
        [Compare("Password")]
        public string ConfirmPassword { get; set; } = string.Empty;

        [DataType(DataType.Text, ErrorMessage = "Not A Valid University Name")]
        public string University { get; set; } = string.Empty;

        [DataType(DataType.MultilineText)]
        public string Description { get; set; } = string.Empty;

        [Display(Name = "Image URL:")]
        [DataType(DataType.ImageUrl, ErrorMessage = "Not A Valid Image URL")]
        public string Image { get; set; } = string.Empty;
    }
}
